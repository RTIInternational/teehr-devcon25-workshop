# Output visualization through Tethys and evaluation customization using TEEHR

## Outline
1. Setup/Intro
2. NGIAB and TEEHR
3. Exploring TEEHR Features
4. Tethys Visualization

## Setup/Intro
### Logging-in to JetStream desktop

First establish an SSH connection:
```bash
ssh -L 5906:localhost:5906 exouser@<ip address>
```

Now in your VNC client go to `localhost:6`

### Cloning the github repos
- Open the terminal (e.g., `ctrl+alt+t`)
- Navigate into the TEEHR workshop folder
```bash
cd workshop/teehr
```
- Clone the visualization repo:
```bash
git clone https://github.com/CIROH-UA/ngiab-client
```

- Clone the TEEHR-DevCon 2025 workshop repo
```bash
git clone https://github.com/RTIInternational/teehr-devcon25-workshop.git
```
- To run TEEHR, navigate into the repo

```bash
cd teehr-devcon2025-workshop
```
This repo contains:
- Readme guides
- Notebooks
- Python scripts and utilities
- `runTeehr.sh`

 ### Take a look at the example NGIAB datasets

- `/home/exouser/workshop/teehr/cat-491334-partial` - Contains pre-executed NGIAB output data.
- `/home/exouser/workshop/teehr/ngen_bm_eval4` - Contains pre-created TEEHR Evaluation dataset.

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

### Check out the TEEHR Documentation!
https://rtiinternational.github.io/teehr/index.html