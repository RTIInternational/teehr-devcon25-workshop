# Coupling TEEHR with NGIAB in a Containerized Environment
## `runTeehr.sh` Options:
- `Last used data directory path`:
  - Path to NGIAB output directory.
- `Select TEEHR run options`: To select/unselect an option, type the number then hit Enter.
  1. Build TEEHR Evaluation
  2. Calculate performance metrics
  3. Launch JupyterLab
  4. Continue
- `Specify the TEEHR image tag to use`:
  - Docker image tag (we'll use the default)
- `Select an option (type a number)`:
  - Use local or remote docker image

<p align="center">
  <img src="images/runTeehr_overview.png">
</p>

### `Execute Notebook` Details:
- `notebooks/01_TEEHR_NGIAB.ipynb`
- `ngiab_utils.py`: Utilities for extracting data from NGIAB output.
- `teehr_utils.py`: Utilities for creating the TEEHR Evaluation dataset.

---

### Option 1. Creating the TEEHR Evaluation
- Primary functions called:
  - `teehr_utils.create_teehr_evaluation()`
    - Create template TEEHR Evaluation
    - Extract and save location and crosswalk files
    - Load locations, crosswalk, configurations
    - Extract and load NGIAB timeseries
    - Fetch and load USGS and NWM v3.0 retro timeseries
  - `ngiab_utils.py`
    - get_gages_from_hydrofabric()
    - get_usgs_nwm30_crosswalk()
    - get_usgs_point_geometry()
    - get_simulation_output_format()
    - get_simulation_start_end_time()
<p align="center">
  <img src="images/create_teehr_evaluation.png">
</p>

---

### Option 2. Calculating Performance Metrics
- `teehr_utils.calculate_metrics()`
<p align="center">
  <img src="images/calculate_metrics.png">
</p>

---

### Option 3. Open Interactive Session
- Opens `01_TEEHR_NGIAB.ipynb` in JupyterLab
