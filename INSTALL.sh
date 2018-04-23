#!/bin/bash

# Read CLI arguments
while getopts "p:t:" opt; do
  case $opt in
    p )
    DB_GEN_ANSWER='yes'
    DB_PATH_ANSWER=$OPTARG
      ;;
    t )
    DB_TYPE_ANSWER=$OPTARG
      ;;
  esac
  done
# Define variables
## Good-bye message
BYE="Thanks for installing mothulity. Hope it will save you as much work as possible! Report bugs and other issues at https://github.com/dizak/mothulity/issues"
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
# Add mothulity to PATH, source it and export PATH just for case
echo "export PATH=\"${MOTHULITY_PATH}:\$PATH\"" >> $BASH_RC
export PATH=$HOME/$MOTHULITY_PATH:$PATH
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
# Check if installer was called with CLI arguments
if [ -n "$DB_PATH_ANSWER" ]; then
  case "$DB_TYPE_ANSWER" in
    1)
    mothulity_dbaser.py $DB_PATH_ANSWER --unite-ITS-02 &&
    mothulity.py . --set-align-database-path "${DB_PATH_ANSWER}/Unite_ITS_02/UNITEv6_sh_99.fasta" --set-taxonomy-database-path "${DB_PATH_ANSWER}/UNITEv6_sh_99.tax"
    ;;
    2)
    mothulity_dbaser.py $DB_PATH_ANSWER --unite-ITS-s-02 &&
    mothulity.py . --set-align-database-path "${DB_PATH_ANSWER}/Unite_ITS_s_02/UNITEv6_sh_97_s.fasta" --set-taxonomy-database-path "${DB_PATH_ANSWER}/UNITEv6_sh_97_s.tax"
    ;;
    3)
    mothulity_dbaser.py $DB_PATH_ANSWER --silva-102 &&
    echo 'Silva-102 is not handled automatically yet. It was NOT set as default database.'
    ;;
    4)
    mothulity_dbaser.py $DB_PATH_ANSWER --silva-119 &&
    mothulity.py . --set-align-database-path "${DB_PATH_ANSWER}/silva.nr_v119.align" --set-taxonomy-database-path "${DB_PATH_ANSWER}/silva.nr_v119.tax"
    ;;
    5)
    mothulity_dbaser.py $DB_PATH_ANSWER --silva-123 &&
    mothulity.py . --set-align-database-path "${DB_PATH_ANSWER}/" --set-taxonomy-database-path "${DB_PATH_ANSWER}/"
    ;;
    *)
    echo 'No such database.'
    ;;
  esac
  exit
fi
# Prompt for databases download
echo "Mothulity needs databases to work its magic. Would you like to download them now?
[yes|no]"
while read DB_GEN_ANSWER
do
  if [ "$DB_GEN_ANSWER" = 'yes' ]; then
    echo 'Where would you like to download it?';
    while read DB_PATH_ANSWER;
    do
      if [ -e "$DB_PATH_ANSWER" ]; then
        echo "It will be set as default database path."
        break
      else
        echo 'Cannot find path. Try again.'
      fi
    done
    echo "Which database would you like to download?
    [1] UNITE ITS 02
    [2] UNITE ITS s 02
    [3] Silva v102
    [4] Silva v119
    [5] Silva v123";
    while read DB_TYPE_ANSWER;
    do
      case "$DB_TYPE_ANSWER" in
        1)
        mothulity_dbaser.py $DB_PATH_ANSWER --unite-ITS-02 &&
        mothulity.py . --set-align-database-path "${DB_PATH_ANSWER}/Unite_ITS_02/UNITEv6_sh_99.fasta" --set-taxonomy-database-path "${DB_PATH_ANSWER}/UNITEv6_sh_99.tax"
        break
        ;;
        2)
        mothulity_dbaser.py $DB_PATH_ANSWER --unite-ITS-s-02 &&
        mothulity.py . --set-align-database-path "${DB_PATH_ANSWER}/Unite_ITS_s_02/UNITEv6_sh_97_s.fasta" --set-taxonomy-database-path "${DB_PATH_ANSWER}/UNITEv6_sh_97_s.tax"
        break
        ;;
        3)
        mothulity_dbaser.py $DB_PATH_ANSWER --silva-102 &&
        echo 'Silva-102 is not handled automatically yet. It was NOT set as default database.'
        break
        ;;
        4)
        mothulity_dbaser.py $DB_PATH_ANSWER --silva-119 &&
        mothulity.py . --set-align-database-path "${DB_PATH_ANSWER}/silva.nr_v119.align" --set-taxonomy-database-path "${DB_PATH_ANSWER}/silva.nr_v119.tax"
        break
        ;;
        5)
        mothulity_dbaser.py $DB_PATH_ANSWER --silva-123 &&
        mothulity.py . --set-align-database-path "${DB_PATH_ANSWER}/" --set-taxonomy-database-path "${DB_PATH_ANSWER}/"
        break
        ;;
        *)
        echo 'No such database.'
        ;;
      esac
    done
    echo $BYE
    exit
  elif [ "$DB_GEN_ANSWER"  = 'no' ]; then
    echo $BYE
    exit
  else
    echo 'Please answer yes or no.'
  fi
done
