# mothulity

Simple tool to facilitate work with [mothur](https://www.mothur.org/).
It can download a proper database, run SOP provided with just fastq files directory, draw few figures and wrap it all into fancy html. Handles slurm and sends e-mail notifications when the job is done (using [headnode_notifier](https://github.com/dizak/headnode_notifier/releases)).


### Installation

1. Requirements.
  * jinja2
  * argparse
  * requests
  * tqdm
  * Biopython
  * matplotlib
  * pylab
  * matplotlib
  * mpld3
  * pandas
  * seaborn

2. External scripts/programs.
  * [headnode_notifier](https://github.com/dizak/headnode_notifier/releases))

3. How to install.
  1. Use python package manager to download dependencies.
  2. Add python scripts to system path.

### Usage

The simplest example is:

```
mothulity.py /path/to/fastq/files -r sh
```

Above command will run MiSeq SOP, draw plots, render html output and zip everything.
