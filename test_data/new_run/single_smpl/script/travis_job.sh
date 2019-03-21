#!/usr/bin/env bash


#SBATCH --job-name="travis_job"
#SBATCH --partition=long
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --exclude=gpu[1-8]



###Create *files file###
mothulity_fc /home/travis/build/dizak/mothulity/test_data/new_run/single_smpl/fastq/ -o /home/travis/build/dizak/mothulity/test_data/new_run/single_smpl/fastq/travis_job.files

###Sequence preprocessing###
mothur '#set.dir(input=/home/travis/build/dizak/mothulity/test_data/new_run/single_smpl/fastq/, output=/home/travis/build/dizak/mothulity/test_data/new_run/single_smpl/fastq/);
set.current(processors=1);

make.contigs(file=travis_job.files);
summary.seqs(fasta=current);

screen.seqs(fasta=current, contigsreport=travis_job.contigs.report, group=current, maxambig=0, maxhomop=8, minoverlap=25, optimize=start-end, criteria=95);

summary.seqs(fasta=current);

unique.seqs(fasta=current);
count.seqs(name=current, group=current);

align.seqs(fasta=current, reference=/home/travis/db/Unite_ITS_02/UNITEv6_sh_99.fasta);
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
classify.seqs(fasta=current, count=current, reference=/home/travis/db/Unite_ITS_02/UNITEv6_sh_99.fasta,
taxonomy=/home/travis/db/Unite_ITS_02/UNITEv6_sh_99.tax, cutoff=80);

remove.lineage(fasta=current, count=current, taxonomy=current, taxon=Chloroplast-Mitochondria-Eukaryota-unknown-Unknown);

cluster.split(fasta=current, count=current, taxonomy=current, cutoff=0.03, large=T, method=agc);


make.shared(list=current, count=current, label=0.03);
classify.otu(list=current, count=current, taxonomy=current, label=0.03);
count.groups(shared=current)'



###Call mothulity for the analysis part###
mothulity /home/travis/build/dizak/mothulity/test_data/new_run/single_smpl/fastq/ -n analysis_travis_job --output-dir /home/travis/build/dizak/mothulity/ --analysis-only -r bash
