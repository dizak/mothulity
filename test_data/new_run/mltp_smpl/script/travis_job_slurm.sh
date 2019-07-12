#!/usr/bin/env bash

#SBATCH --job-name="travis_job_slurm"
#SBATCH --exclusive
#SBATCH --nodes=1
#SBATCH --partition=test

###Create *files file###
mothulity_fc /home/travis/build/dizak/mothulity/test_data/new_run/mltp_smpl/fastq/ -o /home/travis/build/dizak/mothulity/test_data/new_run/mltp_smpl/fastq/travis_job_slurm.files

###Sequence preprocessing###
mothur '#set.dir(input=/home/travis/build/dizak/mothulity/test_data/new_run/mltp_smpl/fastq/, output=/home/travis/build/dizak/mothulity/test_data/new_run/mltp_smpl/fastq/);
set.current(processors=12);

make.contigs(file=travis_job_slurm.files);
summary.seqs(fasta=current);

screen.seqs(fasta=current, contigsreport=travis_job_slurm.contigs.report, group=current, maxambig=0, maxhomop=8, minoverlap=25, optimize=start-end, criteria=95);

summary.seqs(fasta=current);

unique.seqs(fasta=current);
count.seqs(name=current, group=current);

align.seqs(fasta=current, reference=/home/travis/build/dizak/mothulity/test_data/database/t19.align);
summary.seqs(fasta=current, count=current);
screen.seqs(fasta=current, count=current, summary=current,  optimize=start-end, criteria=95);
summary.seqs(fasta=current, count=current);
filter.seqs(fasta=current, vertical=T, trump=.);
unique.seqs(fasta=current, count=current);

summary.seqs(fasta=current, count=current);
pre.cluster(fasta=current, count=current, diffs=2);
chimera.vsearch(fasta=current, count=current, dereplicate=T);
remove.seqs(fasta=current, accnos=current);
summary.seqs(fasta=current, count=current);
classify.seqs(fasta=current, count=current, reference=/home/travis/build/dizak/mothulity/test_data/database/t19.align,
taxonomy=/home/travis/build/dizak/mothulity/test_data/database/t19.tax, cutoff=80);

remove.lineage(fasta=current, count=current, taxonomy=current, taxon=Chloroplast-Mitochondria-Eukaryota-unknown-Unknown);

cluster.split(fasta=current, count=current, taxonomy=current, cutoff=0.03, large=T, method=agc);


remove.rare(list=current, count=current, nseqs=2, label=0.03);
make.shared(list=current, count=current, label=0.03);
classify.otu(list=current, count=current, taxonomy=current, label=0.03);
count.groups(shared=current)'



###Call mothulity for the analysis part###
mothulity /home/travis/build/dizak/mothulity/test_data/new_run/mltp_smpl/fastq/ -n analysis_travis_job_slurm --output-dir /home/travis/build/dizak/mothulity/ --analysis-only -r sbatch
