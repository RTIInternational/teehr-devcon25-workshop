# Output visualization through Tethys and evaluation customization using TEEHR

## Outline
1. Setup -- Intro
2. NGIAB and TEEHR
3. Exploring TEEHR Features
4. Tethys Visualization

## Setup/Intro
- Log-in to JetStream desktop
- Open the terminal (e.g., `ctrl+alt+t`)
- Clone TEEHR-DevCon 2025 repo
```bash
git clone https://github.com/RTIInternational/teehr-devcon25-workshop.git
```
- Navigate into the repo

```bash
cd teehr-devcon2025-workshop
```
- Materials
  - Guides
  - Notebooks
- Sample NGIAB data set(s).
```bash
<NGIAB Output Dir>
├── config
│   ├── <project>_subset.gpkg*
│   ├── cat_config
│   ├── realization.json*
│   └── troute.yaml
├── forcings
│   ├── forcings.nc
│   └── raw_gridded_data.nc
├── metadata
│   └── num_partitions
└── outputs
    ├── ngen
    └── troute
        └── troute_output_<time_period>.nc*
```
\* Needed for TEEHR