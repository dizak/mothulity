# mothulity

Simple script for generating [mothur](https://www.mothur.org/), drawing few figures and wrapping it all into nice-looking html. Handles slurm and sends e-mail notifications when the job is done (using [headnode_notifier](https://github.com/dizak/headnode_notifier/releases)).


### Installation

1. Requirements.
  * Python 2.7
  * jinja2
  * argparse
  * requests as rq
  * tqdm
  * os
  * sys
  * glob
  * Biopython
  * matplotlib
  * pylab
  * matplotlib.pyplot as plt
  * matplotlib.style as style
  * mpld3
  * pandas
  * seaborn

2. External scripts/programs.
  * [headnode_notifier](https://github.com/dizak/headnode_notifier/releases))
  * [mothur_files_creator](https://github.com/dizak/mothur_files_creator/releases)

3. How to install.
  1. Use python package manager to download dependencies.
  2. Add python scripts to system path.

### Usage examples

```
usage: mothulity [OPTION]

creates headnode-suitable mothur script

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -o , --output         output file name. Default <mothur.sh>.
  -n , --job-name       job name. MUST be same as <name>.files. Default
                        <mothur>.
  -m, --mock            use if you have mock community group and want to
                        calculate sequencing errors, classify mock OTUs and
                        draw mock rarefaction curve.
  -r , --run            shell call. Use if you want to run the mothur script
                        immediately, in current directory. eg -r sh for
                        regular bash or -r sbatch for slurm.
  --analysis-only       outputs just the part involved in statistical analysis
                        and drawing.
  -t , --template       path/to/template. Use if you want to use other
                        template than default.

headnode options:
  --partition           headnode's partition. Values: test, short, big, long,
                        accel. Accel necessary for phi/gpu nodes Default
                        <long>.
  --nodes               number of nodes. Default: <1>.
  --ntasks-per-node     number of tasks to invoke on each node. Default <6>
  --mem-per-cpu         maximum amount of real memory per node in gigabytes.
                        Default <24>.
  --node-list           request a specific list of nodes
  --processors          number of logical processors. Default: <24>
  --resources           shortcut for headnode's resources reservation.
                        Accepted values are: <S>mall, <M>edium, <L>arge,
                        <XL>arge for regular nodes with mpi. <PHI> for single
                        phi node, <JUMBO> for two phi nodes. Overrides all the
                        other headnode arguments. Use if you are lazy.
  --notify-email        email address you want to notify when job is done.

mothur options:
  --max-ambig           maximum number of ambiguous bases allowed. screen.seqs
                        param. Default <0>.
  --max-homop           maximum number of homopolymers allowed. screen.seqs
                        param. Default <8>.
  --min-length          minimum length of read allowed. screen.seqs param.
                        Default <400>.
  --max-length          minimum length of read allowed. screen.seqs param.
                        Default <500>.
  --min-overlap         minimum number of bases overlap in contig. screen.seqs
                        param. Default <25>.
  --screen-criteria     trim start and end of read to fit this percentage of
                        all reads. screen.seqs param. Default <95>.
  --chop-length         cut all the reads to this length. Keeps front of the
                        sequences. chop.seqs argument. Default <250>
  --precluster-diffs    number of differences between reads treated as
                        insignificant. screen.seqs param. Default <2>.
  --chimera-dereplicate
                        checking for chimeras by group. chimera.uchime param.
                        Default <T>.
  --classify-seqs-cutoff
                        bootstrap value for taxonomic assignment.
                        classify.seqs param. Default <80>.
  --classify-ITS        removes align.seqs step and modifies classify.seqs
                        with <method=knn>, <search=blast>, <match=2>,
                        <mismatch=-2>, <gapopen=-2>, <gapextend=-1>,
                        <numwanted=1>). Default <False>
  --align-database      path/to/align-database. Used by align.seqs command as
                        <reference> argument. Default
                        <~/db/Silva.nr_v119/silva.nr_v119.align>.
  --taxonomy-database   path/to/taxonomy-database. Used by classify.seqs as
                        <taxonomy> argument. Default
                        <~/db/Silva.nr_v119/silva.nr_v119.tax>
  --cluster-cutoff      cutoff value. Smaller == faster cluster param. Default
                        <0.15>.
  --full-ram-load       Use if you want to use cluster command instead of
                        cluster.split.
  --label               label argument for number of commands for OTU analysis
                        approach. Default 0.03.
  --remove-below        remove groups below this threshold. Omit this argument
                        if you want to keep them all.

drawing options:
  --rarefaction         path/to/rarefaction-file. Use to draw rarefaction
                        curves plot.
  --phylip              path/to/phylip-file. Use to draw heatmap and tree.
  --tree                path/to/tree-file. Use to draw dendrogram.
  --axes                path/to/axes-file. Use to draw scatter plots.
  --summary-table       /path/to/summary-table. Use to convert summary table
                        into fancy DataTable.
  --render-html         path/to/html-template-file. Use to pass args into
                        fancy html.
```
