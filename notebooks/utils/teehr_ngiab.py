
import shutil
from pathlib import Path
from typing import Union
import re
import logging

import teehr
import pandas as pd
import xarray as xr

from utils import ngiab_utils

logger = logging.getLogger(__name__)


def sanitize_string(text):
    """Remove special chars, convert whitespace and hyphens to underscore."""
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]', '_', text)
    return text.lower()


def create_teehr_evaluation(
    teehr_evaluation_dir: Union[str, Path],
    ngiab_output_dir: Union[str, Path],
    temp_dir: Union[str, Path],
    crosswalk_table_filepath: Union[str, Path],
    locations_filepath: Union[str, Path],
    configuration_name: str,
):
    """
    Create a teehr evaluation object with the given parameters.

    """
    shutil.rmtree(teehr_evaluation_dir, ignore_errors=True)

    # ========================================================================
    # Create an Evaluation object and directory, using an empty template.
    # ========================================================================
    ev = teehr.Evaluation(dir_path=teehr_evaluation_dir, create_dir=True)
    ev.clone_template()
    ev.spark.sparkContext.setLogLevel("ERROR")

    # ========================================================================
    # Create the temporary locations and crosswalk tables.
    # ========================================================================
    # Nextgen-USGS
    ngen_usgs_gages = ngiab_utils.get_gages_from_hydrofabric(ngiab_output_dir)
    gages_df = pd.DataFrame(ngen_usgs_gages, columns=["ngen", "usgs"])
    gages_df["usgs"] = "usgs-" + gages_df["usgs"].astype(str)
    # NWM-USGS
    usgs_nwm_xwalk_df = ngiab_utils.get_usgs_nwm30_crosswalk()
    mask = gages_df.usgs.isin(usgs_nwm_xwalk_df.primary_location_id)
    ngen_xwalk_df = gages_df[mask]
    ngen_xwalk_df.rename(
        columns={"ngen": "secondary_location_id", "usgs": "primary_location_id"},  # noqa
        inplace=True
    )
    ngen_xwalk_df["secondary_location_id"] = \
        ngen_xwalk_df.secondary_location_id.str.replace("wb", "ngen")
    # Find the NWMv3.0 ID's corresponding to our NGIAB USGS gage IDs
    mask = usgs_nwm_xwalk_df.primary_location_id.isin(gages_df.usgs)
    nwm_xwalk_df = usgs_nwm_xwalk_df[mask]
    final_xwalk_df = pd.concat(
        [ngen_xwalk_df, nwm_xwalk_df],
        ignore_index=True
    )
    final_xwalk_df.to_parquet(crosswalk_table_filepath, index=False)
    # Create spatial locations layer
    usgs_point_geom = ngiab_utils.get_usgs_point_geometry()
    # Limit it to our gage(s) of interest
    locations_df = usgs_point_geom[usgs_point_geom.id.isin(final_xwalk_df.primary_location_id)]  # noqa
    locations_df.to_parquet(locations_filepath)

    # ========================================================================
    # Load the locations, crosswalk tables, and configurations into TEEHR.
    # ========================================================================
    ev.locations.load_spatial(locations_filepath)
    ev.location_crosswalks.load_parquet(crosswalk_table_filepath)

    ev.configurations.add(
        [
            teehr.Configuration(
                name="usgs_observations",
                type="primary",
                description="USGS Data"
            ),
            teehr.Configuration(
                name="nwm30_retrospective",
                type="secondary",
                description="NWM Data"
            ),
            teehr.Configuration(
                name=configuration_name,
                type="secondary",
                description="Nextgen simulation output"
            )
        ]
    )

    # ========================================================================
    # Load the NGIAB troute timeseries into TEEHR.
    # ========================================================================
    output_format = ngiab_utils.get_simulation_output_format(ngiab_output_dir)
    if output_format == "netcdf":
        pattern = "*.nc"
    elif output_format == "csv":
        pattern = "*.csv"
        raise ValueError("CSV not yet implemented")
    else:
        raise ValueError("Invalid output format!")
    troute_output_file_list = list(
        Path(ngiab_output_dir, "outputs/troute").glob(pattern)
    )
    if len(troute_output_file_list) > 1:
        raise ValueError("More than one output file was found!")

    troute_output_nc_filepath = troute_output_file_list[0]
    troute_ds = xr.open_dataset(troute_output_nc_filepath)
    troute_subset_filepath = Path(temp_dir, "troute_output_subset.nc")
    # Subset the troute output to only the gages of interest
    ngen_gages = [int(gage.split("-")[1]) for gage in final_xwalk_df.secondary_location_id.tolist() if gage.split("-")[0] == "ngen"]
    troute_ds.sel(feature_id=ngen_gages).to_netcdf(troute_subset_filepath)

    ev.secondary_timeseries.load_netcdf(
        in_path=troute_subset_filepath,
        field_mapping={
            "time": "value_time",
            "feature_id": "location_id",
            "flow": "value"
        },
        constant_field_values={
            "unit_name": "m^3/s",
            "variable_name": "streamflow_hourly_inst",
            "configuration_name": configuration_name,
            "reference_time": None
        },
        location_id_prefix="ngen"
    )

    # ========================================================================
    # Fetch and load the NWM and USGS streamflow timeseries into TEEHR.
    # ========================================================================
    start_date, end_date = ngiab_utils.get_simulation_start_end_time(
        ngiab_output_dir
    )
    # USGS
    ev.fetch.usgs_streamflow(
        start_date=start_date,
        end_date=end_date
    )
    # NWM
    ev.fetch.nwm_retrospective_points(
        nwm_version="nwm30",
        variable_name="streamflow",
        start_date=start_date,
        end_date=end_date
    )

    ev.joined_timeseries.create(execute_scripts=False)


def calculate_metrics(
    teehr_evaluation_dir: Union[str, Path],
    metrics_csv_filepath: Union[str, Path]
):
    """
    Calculate metrics for the given teehr evaluation directory.

    """
    if not Path(teehr_evaluation_dir).exists():
        raise ValueError(
            "The TEEHR evaluation directory does not exist. "
            "Please run option 1 first."
        )

    # ========================================================================
    # Initialize the TEEHR Evaluation.
    # ========================================================================
    logger.info("Initializing teehr evaluation")
    ev = teehr.Evaluation(dir_path=teehr_evaluation_dir)
    ev.spark.sparkContext.setLogLevel("ERROR")
    # ev.enable_logging()

    # ========================================================================
    # Specify the metrics, the data population(s), and execute the query.
    # ========================================================================
    logger.info("Calculating metrics")
    # Calculate some metrics
    df = ev.metrics.query(
        order_by=["primary_location_id", "configuration_name"],
        group_by=["primary_location_id", "configuration_name"],
        include_metrics=[
            teehr.DeterministicMetrics.KlingGuptaEfficiency(),
            teehr.DeterministicMetrics.NashSutcliffeEfficiency(),
            teehr.DeterministicMetrics.RelativeBias(),
            teehr.DeterministicMetrics.RootMeanStandardDeviationRatio()
        ]
    ).to_pandas()

    # ========================================================================
    # Save the results to a CSV file in the NGIAB directory.
    # ========================================================================
    df.to_csv(metrics_csv_filepath, index=False)
