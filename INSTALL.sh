#!/usr/bin/env bash

# Define variables
## Where is ~/.bashrc
BASH_RC=${HOME}/.bashrc
echo $BASH_RC
## Where is conda
CONDA_PATH=$(which conda)
echo $CONDA_PATH
## Where is mothulity
MOTHULITY_PATH=$(dirname $0)
echo $MOTHULITY_PATH
# Check for Anaconda
if [ ${#CONDA_PATH} -eq 0 ]; then
  echo 'Please install Anaconda first.';
  exit;
else echo "Found Anaconda in: ${CONDA_PATH}";
fi
# Add mothulity to PATH
# Create mothulity env from mothulity.yaml
if [ "$CONDA_PATH"==*"$HOME"* ]; then
  echo "conda env create --file /path/to/mothulity.yaml"
else echo "mkdir "${MOTHULITY_PATH}/env"";
  echo "${HOME}/${MOTHULITY_PATH}"
fi
