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

### Clone the github repo
- Open the terminal (e.g., `ctrl+alt+t`)
- Clone TEEHR-DevCon 2025 repo
```bash
git clone https://github.com/RTIInternational/teehr-devcon25-workshop.git
```
- Navigate into the repo

```bash
cd teehr-devcon2025-workshop
```
The repo contains:
- Readme guides
- Notebooks
- Python scripts and utilities
- `runTeehr.sh`

 ### Take a look at the example NGIAB datasets

- `/home/exouser/workshop/teehr/Example1...`
- `/home/exouser/workshop/teehr/Example2...`

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