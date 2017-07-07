#!/usr/bin/env bash

# Define variables
## Where is ~/.bashrc
BASH_RC=${HOME}/.bashrc
echo $BASH_RC
## Where is conda
CONDA_PATH=$(which conda)
echo $CONDA_PATH
## Go to mothulity directory and get its absolute path
cd $(dirname $0)
MOTHULITY_PATH=$(pwd)
echo $MOTHULITY_PATH
# Check for Anaconda
if [ ${#CONDA_PATH} -eq 0 ]; then
  echo 'Please install Anaconda first.';
  exit;
else echo "Found Anaconda in: ${CONDA_PATH}";
fi
# Backup .bashrc before editing it
echo "cp $BASH_RC "${BASH_RC}.bak""
# Add mothulity to PATH and source it
echo "export PATH=\"${MOTHULITY_PATH}:\$PATH\" >> $BASH_RC"
echo "source ${BASH_RC}"
# Create mothulity env from mothulity.yaml
echo "conda env create --file "${MOTHULITY_PATH}/mothulity.yaml"";
# Get python interpreter's location from the env
echo "source activate mothulity"
ENV_PYTHON=$(which python)
echo $ENV_PYTHON
# Replace shebangs in *py files in mothulity directory
for i in "${MOTHULITY_PATH}/*.py"; do
  echo "sed -i 's@/usr/bin/env python@$ENV_PYTHON@g' ${i}";
done
