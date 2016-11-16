#!/bin/bash
##SBATCH --job-name="zury_V3_V4"
##SBATCH --partition=
##SBATCH --nodes=
##SBATCH --ntasks-per-node=
##SBATCH --mem-per-cpu=
##SBATCH --nodelist=

mothur '#set.current(processors=8); make.contigs(file=zury_V3_V4.files); summary.seqs(fasta=current); screen.seqs(fasta=current, contigsreport=zury_V3_V4.contigs.report, group=current, summary=current, maxambig=0, maxhomop=8, minlength=400, maxlength=500, minoverlap=25); summary.seqs(fasta=current); unique.seqs(fasta=current); count.seqs(name=current, group=current); summary.seqs(fasta=current, count=current); align.seqs(fasta=current, reference=/home/dizak/db/Silva.nr_v119/silva.nr_v119.align); summary.seqs(fasta=current, count=current); screen.seqs(fasta=current, count=current, summary=current, start=6428, end=23440); summary.seqs(fasta=current, count=current); filter.seqs(fasta=current, vertical=T, trump=.); unique.seqs(fasta=current, count=current); summary.seqs(fasta=current, count=current); pre.cluster(fasta=current, count=current, diffs=4); chimera.uchime(fasta=current, count=current, dereplicate=T); remove.seqs(fasta=current, accnos=current); summary.seqs(fasta=current, count=current); classify.seqs(fasta=current, count=current, reference=/home/dizak/db/Silva.nr_v119/silva.nr_v119.align, taxonomy=/home/dizak/db/Silva.nr_v119/silva.nr_v119.tax, cutoff=80); remove.lineage(fasta=current, count=current, taxonomy=current, taxon=Chloroplast-Mitochondria-Eukaryota-unknown-Unknown); cluster.split(fasta=current, count=current, taxonomy=current, splitmethod=classify, taxlevel=4, cutoff=0.03); make.shared(list=current, count=current, label=0.03); classify.otu(list=current, count=current, taxonomy=current, label=0.03); count.groups(shared=current)'
