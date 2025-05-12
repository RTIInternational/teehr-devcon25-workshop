# Coupling TEEHR with NGIAB in a Containerized Environment
## `runTeehr.sh` Options:
- Path to NGIAB output directory.
- TEEHR run options.
  - Build TEEHR Evaluation
  - Calculate performance metrics
  - Launch JupyterLab
- Docker image tag
- Use local or remote docker image

<img src="images/runTeehr_overview.svg">

## Notebook Execution Details
- `notebooks/01_TEEHR_NGIAB.ipynb`
- `ngiab_utils.py`: Utilities for extracting data from NGIAB output.
- `teehr_utils.py`: Utilities for creating the TEEHR Evaluation dataset.

### 1. Creating the TEEHR Evaluation
- `teehr_utils.create_teehr_evaluation()`
- `ngiab_utils.py`
<img src="images/create_teehr_evaluation.svg">


### 2. Calculating Performance Metrics
- `teehr_utils.calculate_metrics()`

<img src="images/calculate_metrics.svg">


### 3. Open Interactive Session
- Opens JupyterLab
