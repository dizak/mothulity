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
# Create regular mothulity env from mothulity.yaml
conda env create --file "${MOTHULITY_PATH}/mothulity.yaml" --force
# Create no-mothur mothulity env from mothulity_sm.yaml
conda env create --file "${MOTHULITY_PATH}/mothulity_sm.yaml" --force
# Get python interpreter's location from the env
. activate mothulity
ENV_PYTHON=$(which python)
# Replace shebangs in *py files in mothulity directory
for i in "${MOTHULITY_PATH}/*.py"; do
  sed -i "s@/usr/bin/env python@${ENV_PYTHON}@g" $i;
done
# Run doc tests in all the python files
for i in "${MOTHULITY_PATH}/*.py"; do
  python -m doctest $i -v;
done
# Go to mothulity directory
cd $MOTHULITY_PATH
# Run unittests
python -m unittest -v tests.tests;
# Prompt for databases download
echo 'Mothulity needs databases to work its magic. Would you like to download them now? [yes|no].
You can always download the databases later with mothulity_dbaser.py and set the default database path with
mothulity.py --set-align-database-path and
mothulity.py --set-taxonomy-database-path'
read DB_GEN_ANSWER;
if [ $DB_GEN_ANSWER -eq 'yes' ]; then
  echo 'Which database would you like to download?
[UNITE ITS 02|UNITE ITS s 02|Silva v102|Silva v119|Silva v123]'
  read DB_TYPE_ANSWER;
  echo 'Where would you like to download it? It will be set as default database mothulity path.'
  read DB_PATH_ANSWER;
  case $DB_TYPE_ANSWER in
    "UNITE ITS 02") mothulity_dbaser.py /path/to/databases $DB_PATH_ANSWER --unite-ITS-02; mothulity.py . --set-align-database-path "${DB_PATH_ANSWER}/Unite_ITS_02/UNITEv6_sh_99.fasta" --set-taxonomy-database-path "${DB_PATH_ANSWER}/UNITEv6_sh_99.tax"
    "UNITE ITS s 02") mothulity_dbaser.py /path/to/databases $DB_PATH_ANSWER --unite-ITS-s-02; mothulity.py . --set-align-database-path "${DB_PATH_ANSWER}/Unite_ITS_s_02/UNITEv6_sh_97_s.fasta" --set-taxonomy-database-path "${DB_PATH_ANSWER}/UNITEv6_sh_97_s.tax"
    "Silva v102") mothulity_dbaser.py /path/to/databases $DB_PATH_ANSWER --silva-102; mothulity.py . --set-align-database-path "${DB_PATH_ANSWER}/" --set-taxonomy-database-path "${DB_PATH_ANSWER}/"
    "Silva v119") mothulity_dbaser.py /path/to/databases $DB_PATH_ANSWER --silva-119; mothulity.py . --set-align-database-path "${DB_PATH_ANSWER}/silva.nr_v119.align" --set-taxonomy-database-path "${DB_PATH_ANSWER}/silva.nr_v119.tax"
    "Silva v123") mothulity_dbaser.py /path/to/databases $DB_PATH_ANSWER --silva-123; mothulity.py . --set-align-database-path "${DB_PATH_ANSWER}/" --set-taxonomy-database-path "${DB_PATH_ANSWER}/"
fi
