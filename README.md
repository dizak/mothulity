# mothulity

Simple tool to facilitate work with [mothur](https://www.mothur.org/).
It can download a proper database, run SOP provided with just fastq files directory, draw few figures and wrap it all into fancy html. Handles slurm and sends e-mail notifications when the job is done (using [headnode_notifier](https://github.com/dizak/headnode_notifier/releases)).


### Installation

Add /path/to/mothulity to you system path.

### Requirements

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
  * [headnode_notifier](https://github.com/dizak/headnode_notifier/)
  * [KronaTools](https://github.com/marbl/Krona)


### Usage

[Anaconda](https://anaconda.org) users: remmember to **activate you environment!**

```
source activate mothulity
```

The simplest example is:

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


### Databases


You can easily download Silva and Unite databases with mothulity_db.py.
Please type ```mothulity_db.py --help``` for details.

Databases downloaded with mothulity_db to ```~/db/``` should be found by mothulity by default.
If using something else, specify ```/path/to/database``` with ```--align-database``` and ```--taxonomy-database``` when running mothulity main script.


### Example data

Presumably, it is a good idea to test mothulity with [MiSeq SOP](https://mothur.org/w/images/d/d6/MiSeqSOPData.zip) delivered by creators of  [mothur](https://www.mothur.org/).
