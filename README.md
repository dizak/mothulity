[![Build Status](https://travis-ci.org/dizak/mothulity.svg?branch=master)](https://travis-ci.org/dizak/mothulity)


# mothulity

Simple tool to facilitate work with [mothur](https://www.mothur.org/).
It can download a proper database, run SOP provided with just fastq files directory, draw few figures and wrap it all into fancy html. Handles slurm and sends e-mail notifications when the job is done (using [headnode_notifier](https://github.com/dizak/headnode_notifier/releases)).


### Installation

1. Install [Anaconda](https://anaconda.org).
2. ```git clone https://github.com/dizak/mothulity```.
3. ```bash INSTALL.sh```


### Update

```
bash UPDATE.sh
```


### Usage

#### Databases

mothulity needs databases to operate. Databases can be placed anywhere. The paths should be
specified by the CLI or in the config file. CLI overrides the config file settings.
User is asked whether download and set default paths during installation.

- Databases download is handled by ```mothulity_dbaser.py /path/where/database/should/be/downloaded --type-of-database```, eg ```mothulity_dbaser.py /home/user/mothulity/dbs --silva-119```.

- Databases default path set-up is handled by ```mothulity.py --set-align-database-path /path/to/database --set-taxonomy-database-path```.

#### Basic usage

```
mothulity.py /path/to/fastq/files -r sh
```

Above command will run MiSeq SOP, draw plots, render html output and zip everything.
Omit ```-r``` if you do not want the produced bash script to be executed.
The ```-r``` option accepts any shell of choice. On a regular Linux machine it will be probably ```-r sh```. On, let's say SLURM Queueing System: ```-r -sbatch```. On TORQUE: ```-r qsub```. Mothulity does not really care, it is the matter of the user's system.

You can send results in the email notification with:

```
mothulity.py /path/to/fastq/files -r sh --notify-email your.email@your.domain
```

As ```--notify-email``` depends on [headnode_notifier](https://github.com/dizak/headnode_notifier/), please check its repo for configuration instructions.


### Example data

Presumably, it is a good idea to test mothulity with [MiSeq SOP](https://mothur.org/w/images/d/d6/MiSeqSOPData.zip) delivered by creators of  [mothur](https://www.mothur.org/).


### Requirements for manual installation

* [Anaconda](https://anaconda.org) users: install dependencies with

  ```
  conda env create --file /path/to/mothulity.yaml
  ```
  or if you have access restrictions (eg. anaconda is installed system-wide)

  ```
  conda env create --file /path/to/mothulity.yaml -p /your/path/to/env/
  ```

  and that's all.

* non-conda users: beside installing packages listed in mothulity.yaml, you need:
  * [mothur](https://mothur.org/)
  * [KronaTools](https://github.com/marbl/Krona)
  * [headnode_notifier](https://github.com/dizak/headnode_notifier/)
