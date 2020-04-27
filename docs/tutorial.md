---
layout: default
---

# Tutorial


## Table of Contents

[Minimal Example](#minimal-example)

[Prerequisities](#prerequisities)

[Installing](#installing)

[Downloading Databases](#downloading-databases)

[Setting Persistent Database Path](#setting-persistent-database-path)

[Running Analysis](#running-analysis)

[Slurm Workload Manager](#slurm-md)

[Minified Test-Run Dataset](#minified-test-run-dataset)

```mothulity``` is simple to use. Nevertheless, it won't hurt to show some brief usage example.


## Minimal Example


Below you can find a minimal example of installation, setting things up and usage.
It should be self-explainatory. If not - each step is explained in the subsequent sections.


```bash
mkdir databases_directory
pip install --user mothulity
mothulity_dbaser databases_directory --silva-119
mothulity --set-align-database-path databases_directory/silva.nr_v119.align
mothulity --set-taxonomy-database-path databases_directory/silva.nr_v119.tax
mothulity project/fastq/directory -r bash -n my_first_mothulity_project
```


## Prerequisities


1. In this brief tutorial we will assume you are working in your ```$HOME``` directory.

1. Create a directory for storing databases. For our example, let it be ~/databases_directory.

1. Download the [test dataset](https://www.mothur.org/w/images/d/d6/MiSeqSOPData.zip) to your home directory and unzip it.

1. ```mothulity``` uses a simple naming convention for the input fastq files. Have a look at two pairs of files inside ```~/MiSeq_SOP```:

```bash
F3D0_S188_L001_R1_001.fastq
F3D0_S188_L001_R2_001.fastq
F3D1_S189_L001_R1_001.fastq
F3D1_S189_L001_R2_001.fastq
```

this is how mothulity sees it:

|Sample name|Direction|Extension|
|:----------|:--------|:--------|
|F3D0       |R1       |fastq    |
|F3D0       |R2       |fastq    |
|F3D1       |R1       |fastq    |
|F3D1       |R2       |fastq    |

  * The separator is ```_```.
  * The sample name is the first part of the name.
  * ```R1``` means *forward* and ```R2``` means *backward*.
  * ```fastq``` extension means it is a valid file to take as an input.

## Installing


```mothulity``` is available as Python package. It can be installed with pip:


```bash
pip install --user mothulity
```


```mothulity``` comes with [Mothur](https://mothur.org/wiki/Main_Page) bundled.
If you are fine with this, go ahead and install it system-wide.
Nevertheless, it is a good practise to install software in a separate, [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/).
Moreover, there is still an ongoing debate over where ```pip``` is supposed to store data files (on which ```mothulity``` depends heavily).
The behaviour of ```pip``` in this matter can vary in different distributions.
It is highly recommended that you use the ```--user``` option outside ```virtualenv```.


## Downloading Databases


There would be no 16S/ITS analysis with a database.
```mothulity_dbaser``` can help with that - give it a path where you want your files to be downloaded and type of the database.


### Example


```bash
mothulity_dbaser ~/databases_directory --silva-119
```


## Setting Persistent Database Path


```mothulity``` needs to know where the databases live.You can specify the path each time you run the analysis using arguments:



```bash
--align-database ~/databases_directory/silva.nr_v119.align
```


and


```bash
--taxonomy-database ~/databases_directory/silva.nr_v119.tax
```


or you can set it persistently with commands:


```bash
mothulity --set-align-database-path ~/databases_directory/silva.nr_v119.align
```


and


```bash
mothulity --set-taxonomy-database-path ~/databases_directory/silva.nr_v119.tax
```


## Running Analysis


Once the databases path is set up, you can easily run your analysis:

```bash
mothulity ~/MiSeq_SOP -r bash -n my_first_mothulity_project
```

```~/MiSeq_SOP``` is where your fastq files are.

```-r bash``` indicates shell to use. If you are using some *exotic* shell, pass its name here. If you are using workload manager, use a command to submit a job. For [SLURM](https://slurm.schedmd.com/) it would be ```sbatch```

```-n my_first_mothulity_project``` is used to name files, directories and give a title the final output.

The output is placed in ```~/MiSeq_SOP/analysis/OTU/analysis_my_first_mothulity_project.html``` and should look like [this](./analysis-example/analysis-my-first-mothulity-project.html)


## [Slurm Workload Manager](https://www.schedmd.com)


```mothulity``` can be conveniently used with [Slurm Workload Manager](https://www.schedmd.com) so it is good idea to use it on your HPC/computing facility. It requires two steps:

1. Configuration of your queues/jobs.

1. Specifying the ```sbatch``` as shell to run.

There are three options to manage [Slurm Workload Manager](https://www.schedmd.com):

1.```--add-slurm-setting```

1.```--list-slurm-settings```

1. ```--use-slurm-setting```

The user is free to go with any configuration really. A real-life example might be:

1.
```bash
mothulity --add-slurm-setting "name=big_queue partition=long processors=32 exclusive"
```

The options specified here are used as SBATCH flags. The ```name``` keyword is reserved and is used to call the desired settings later on. The setting is permanent. Another setting with the same name would **overwrite the previous one**!

1.
```bash
mothulity ~/MiSeq_SOP -n my_first_mothulity_project -r sbatch --use-slurm-setting big_queue
```

This tells ```mothulity``` to run the analysis using [SLURM](https://slurm.schedmd.com/) with previously defined ```big_queue``` settings. It renders:


```bash
#SBATCH --job-name="my_first_mothulity_project"
#SBATCH --partition=test
#SBATCH --exclusive
```

and puts it before the rest of the script that runs [Mothur](https://mothur.org/wiki/Main_Page)

1. If you want to what settings are already saved - type:

```bash
mothulity --list-slurm-settings
```

## Minified Test-Run Dataset

The above example uses real data (real means any interpretation makes sense in real world) and real databases.
If you just want to test if everything works as expected save yourself time and RAM, then you can use ```mothulity``` built-in test-run dataset.
If ```mothulity``` is correctly installed - you do not need to download anything.
Just type:

```bash
mothulity --get-test-run-data
```

It copies the test_run_database test_run_samples directories into your ```CWD```.
The procedure work just the same as described above, the files are just much, much smaller.
