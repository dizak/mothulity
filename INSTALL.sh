#!/bin/bash

_db_answer=''
_path_export=''

### Read CLI arguments

while getopts ":p:t:y" opt; do
  case $opt in
    p )
    _db_answer='yes'
    _db_path=$OPTARG
      ;;
    t )
    _db_type=$OPTARG
      ;;
    y )
    _path_export='yes'
      ;;
    \? )
    printf "Invalid option: -$OPTARG.
    Execute script without any additional arguments to perform guided
    installation.

    To predefine installation parameters use following arguments:
    - p <database_output_path>
    - t <database_id>

    Available databases [ID]:
    [1] UNITE ITS 02
    [2] UNITE ITS s 02
    [3] Silva v102
    [4] Silva v119
    [5] Silva v123
    "
    exit 1
      ;;
  esac
done

### Download database function

download_database() {
  # $1 = ${_db_type}
  # $2 = ${_db_path}
  case $1 in
    1)
    ./mothulity_dbaser.py "${2}" --unite-ITS-02 &&
    ./mothulity.py . --set-align-database-path "${2}/Unite_ITS_02/UNITEv6_sh_99.fasta" --set-taxonomy-database-path "${2}/UNITEv6_sh_99.tax"
    ;;
    2)
    ./mothulity_dbaser.py "${2}" --unite-ITS-s-02 &&
    ./mothulity.py . --set-align-database-path "${2}/Unite_ITS_s_02/UNITEv6_sh_97_s.fasta" --set-taxonomy-database-path "${2}/UNITEv6_sh_97_s.tax"
    ;;
    3)
    ./mothulity_dbaser.py "${2}" --silva-102 &&
    printf 'Silva-102 is not handled automatically yet.
    It was NOT set as default database.\n'
    ;;
    4)
    ./mothulity_dbaser.py "${2}" --silva-119 &&
    ./mothulity.py . --set-align-database-path "${2}/silva.nr_v119.align" --set-taxonomy-database-path "${2}/silva.nr_v119.tax"
    ;;
    5)
    ./mothulity_dbaser.py "${2}" --silva-123 &&
    ./mothulity.py . --set-align-database-path "${2}/" --set-taxonomy-database-path "${2}/"
    ;;
    6)
    break
    ;;
    *)
    printf "\nNo such database.\n"
    printf "${_db_choice_msg}"
    ;;
  esac

}

### Verify path existence function

verify_path(){
  # $1 = _db_path
  if [ -e "$1" ]; then
    printf "$1 will be set as default database path.\n"
    break
  else
    printf "Given path doesn't exist.\n"
  fi
}

### Add path to .bashrc function
add_path(){
  # $1 = _mothulity_path
  # ~/.bashrc path
  _bashrc_path=${HOME}/.bashrc
  # Backup .bashrc before editing it
  cp ${_bashrc_path} "${_bashrc_path}.bak"
  # Add mothulity to PATH, source it and export PATH just for case
  echo "export PATH=\"$1:\$PATH\"" >> ${_bashrc_path}
  export PATH=$HOME/$1:$PATH
  . ${_bashrc_path}
  printf "mothulity location added to PATH in your .bashrc.\n\n"
}
### Define variables

_bye_msg="\nThanks for installing mothulity. Hope it will save you as much work as possible!
Report bugs and other issues at https://github.com/dizak/mothulity/issues.\n"
_db_choice_msg="\nWhich database would you like to download?
[1] UNITE ITS 02
[2] UNITE ITS s 02
[3] Silva v102
[4] Silva v119
[5] Silva v123
[6] Exit \n"
# mothulity path
cd $(dirname $0)
_mothulity_path=$(pwd)
# is Anaconda installed
_conda_path=$(which conda)
if [ ${#_conda_path} -eq 0 ]; then
  printf 'Please install Anaconda first.\n';
  exit
else
  printf "Found Anaconda in: ${_conda_path}.\n";
fi

### Add mothulity to PATH in .bashrc
if [ ! -z "$_path_export" ]; then
  add_path "${_mothulity_path}"
else
  printf "\nDo you wish the installer to add mothulity location to PATH in your ~/.bashrc?
[yes|no]\n"
  while read _path_export; do
    if [ "${_path_export}" = 'yes' ]; then
      add_path "${_mothulity_path}"
      break
    elif [ "${_path_export}" = 'no' ]; then
      printf "You may wish to edit your .bashrc "
      printf "or export the mothulity location to PATH later.\n\n"
      break
    else
      printf "Unknown option. Type 'yes' or 'no'.\n"
    fi
  done
fi

### Set up and test mothulity

# Create regular mothulity env from mothulity.yaml
conda env create --file "${_mothulity_path}/mothulity.yaml" --force
# Get python interpreter's location from the env
. activate mothulity
ENV_PYTHON=$(which python)
# Replace shebangs in *py files in mothulity directory
for i in "${_mothulity_path}/*.py"; do
  sed -i "s@/usr/bin/env python@${ENV_PYTHON}@g" $i;
done

### Setting up output path
if [ ! -z "$_db_answer" ]; then
  if [ ! -e "$_db_path" ]; then
  printf "Predefined <database_output_path> doesn't exist.\n\n"
  _db_answer=""
  fi
fi

if [ -z "$_db_answer" ]; then
  printf "Mothulity needs databases to work its magic. Would you like to download them now?
[yes|no]\n"
  while read _db_answer; do
    if [ "${_db_answer}" = 'yes' ]; then
      printf "Where would you like to download it?\n"
      while read _db_path; do
        verify_path "${_db_path}"
      done
      break
    elif [ "${_db_answer}" = 'no' ]; then
      printf "${_bye_msg}"
      exit
    fi
  done
fi

if [ ! -z "$_db_type" ]; then
    download_database "${_db_type}" "${_db_path}"
else
    printf "${_db_choice_msg}"
fi

printf "${_bye_msg}"
exit
