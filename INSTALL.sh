#!/usr/bin/env bash

# Define variables
## Where is ~/.bashrc
BASH_RC=${HOME}/.bashrc
## Where is conda
CONDA_PATH=$(which conda)
## Go to mothulity directory and get its absolute path
cd $(dirname $0)
MOTHULITY_PATH=$(pwd)
# Check for Anaconda
if [ ${#CONDA_PATH} -eq 0 ]; then
  echo 'Please install Anaconda first.';
  exit;
else echo "Found Anaconda in: ${CONDA_PATH}";
fi
# Backup .bashrc before editing it
cp $BASH_RC "${BASH_RC}.bak"
# Add mothulity to PATH and source it
echo "export PATH=\"${MOTHULITY_PATH}:\$PATH\"" >> $BASH_RC
. ${BASH_RC}
# Create mothulity env from mothulity.yaml
conda env create --file "${MOTHULITY_PATH}/mothulity.yaml" --force
# Get python interpreter's location from the env
. activate mothulity
ENV_PYTHON=$(which python)
# Replace shebangs in *py files in mothulity directory
for i in "${MOTHULITY_PATH}/*.py"; do
  sed -i "s@/usr/bin/env python@${ENV_PYTHON}@g" $i;
done
