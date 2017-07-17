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
# Check for mothulity
if [ ${#MOTHULITY_PATH} -eq 0 ]; then
  echo 'Cannot find mothulity in your $PATH. Please install mothulity first.';
  exit;
else echo "Found mothulity in: ${MOTHULITY_PATH}";
fi
# Go to mothulity directory and pull from git
cd $MOTHULITY_PATH
git fetch --all
git reset --hard origin/master
# Remove old env and create new
conda env create --file "${MOTHULITY_PATH}/mothulity.yaml" --force
# Get python interpreter's location from the env
. activate mothulity
ENV_PYTHON=$(which python)
# Replace shebangs in *py files in mothulity directory
for i in "${MOTHULITY_PATH}/*.py"; do
  sed -i "s@/usr/bin/env python@${ENV_PYTHON}@g" $i;
done
