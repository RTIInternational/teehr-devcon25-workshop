#!/bin/bash
if [ "$1" == "run_teehr" ]; then
    # jupyter nbconvert --to notebook --execute /app/notebooks/01_TEEHR_NGIAB.ipynb --inplace
    papermill /app/notebooks/01_TEEHR_NGIAB.ipynb /app/notebooks/01_TEEHR_NGIAB.ipynb --progress-bar --log-output --log-level INFO --cwd /app/notebooks
elif [ "$1" == "run_jupyter" ]; then
    jupyter lab --ip=0.0.0.0 --port=8888 --allow-root --notebook-dir=/app/notebooks --no-browser --NotebookApp.token='' --NotebookApp.password=''
else
    echo "Error: Invalid argument."
    exit 1
fi