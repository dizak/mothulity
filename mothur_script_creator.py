#! /usr/bin/env python

import jinja2 as jj2
import argparse
import requests as rq
from tqdm import tqdm
import os
import sys
from Bio import Phylo as ph
import pylab
import matplotlib.pylot as plt
import matplotlib.style as style
import mpld3
from pandas import read_csv
from seaborn import heatmap
from seaborn import pairplot
from seaborn import lmplot

__author__ = "Dariusz Izak IBB PAS"
__veersion = "0.9.1"


def load_template_str(template_str):
    template = jj2.Environment().from_string(template_str)
    return template


def load_template(template_file):
    template_Loader = jj2.FileSystemLoader(searchpath = ".")
    template_Env = jj2.Environment(loader = template_Loader)
    template = template_Env.get_template(template_file)
    return template


def render_template(template_loaded,
                    job_name = "mothur.job",
                    mock = False,
                    analysis_only = False,
                    partition = "long",
                    nodes = 1,
                    ntasks_per_node = 6,
                    mem_per_cpu = 24,
                    node_list = None,
                    processors = 12,
                    max_ambig = 0,
                    max_homop = 8,
                    min_length = 400,
                    max_length = 500,
                    min_overlap = 25,
                    screen_criteria = 95,
                    chop_length = 250,
                    precluster_diffs = 4,
                    chimera_dereplicate = "T",
                    classify_seqs_cutoff = 80,
                    align_database = None,
                    taxonomy_database = None,
                    cluster_cutoff = 0.15,
                    label = 0.03):
    mem_per_cpu = "{0}G".format(mem_per_cpu)
    msc_path = sys.argv[0]
    template_vars = {"msc_path": msc_path,
                     "job_name": job_name,
                     "mock": mock,
                     "analysis_only": analysis_only,
                     "partition": partition,
                     "nodes": nodes,
                     "ntasks_per_node": ntasks_per_node,
                     "mem_per_cpu": mem_per_cpu,
                     "node_list": node_list,
                     "processors": processors,
                     "max_ambig": max_ambig,
                     "max_homop": max_homop,
                     "min_length": min_length,
                     "max_length": max_length,
                     "min_overlap": min_overlap,
                     "screen_criteria": screen_criteria,
                     "chop_length": chop_length,
                     "precluster_diffs": precluster_diffs,
                     "chimera_dereplicate": chimera_dereplicate,
                     "classify_seqs_cutoff": classify_seqs_cutoff,
                     "align_database": align_database,
                     "taxonomy_database": taxonomy_database,
                     "cluster_cutoff": cluster_cutoff,
                     "label": label}
    template_rendered = template_loaded.render(template_vars)
    return template_rendered


def save_template(out_file_name,
                  template_rendered):
    with open(out_file_name, "w") as fout:
        fout.write(template_rendered)


def save_template(out_file_name,
                  template_rendered):
    with open(out_file_name, "w") as fout:
        fout.write(template_rendered)


def get_db(url,
           save_path,
           chunk = 8192):
    res = rq.get(url, stream = True)
    total_len = int(res.headers.get("content-length"))
    if res.status_code == 200:
        with open(save_path, "wb") as fout:
            for i in tqdm(res.iter_content(chunk_size = chunk),
                          total = total_len / chunk):
                fout.write(i)
    else:
        pass


def draw_rarefaction(file_name):
    output_file("{}.bokeh.html".format(file_name))
    df = read_csv(file_name,
                  sep = "\t",
                  index_col = "numsampled")
    cols = [i for i in df.columns if "lci" not in i]
    cols = [i for i in cols if "hci" not in i]
    df = df[cols]
    fig, ax = plt.subplots()
    df[cols].plot(ax = ax,
                  figsize = (15, 8))
    labels = list(df.columns.values)
    for i in range(len(labels)):
        tooltip = mpld3.plugins.LineLabelTooltip(ax.get_lines()[i],
                                                 labels[i])
        mpld3.plugins.connect(plt.gcf(), tooltip)
    plt.grid(True)
    plt.title("Rarefaction curve")
    plt.ylabel("OTU count at 0.03 cutoff")
    plt.xlabel("hundreds of sequences")
    with open("mpld3.html", "w") as fout:
    fout.write(mpld3.fig_to_html(fig))

def draw_heatmap(file_name):
    df = read_csv(file_name,
                  sep="\t",
                  skiprows=1,
                  header=None,
                  index_col=0)
    df.columns = df.index
    fig = heatmap(df, square=True, cmap="plasma").get_figure()
    fig.savefig("{}.svg".format(file_name))


def draw_tree(file_name):
    pylab.ion()
    tree = ph.read(file_name, "newick")
    ph.draw(tree)
    pylab.savefig("{}.svg".format(file_name))


def draw_scatter(file_name):
    df = read_csv(file_name,
                  sep="\t")
    fig = lmplot(x="axis1",
                 y="axis2",
                 data=df,
                 hue="group",
                 fit_reg=False)
    fig.savefig("{}.svg".format(file_name))


def main():
    templ_str_otu = """#!/bin/bash

#SBATCH --job-name="{{job_name}}"
#SBATCH --partition={{partition}}
#SBATCH --nodes={{nodes}}
#SBATCH --ntasks-per-node={{ntasks_per_node}}
#SBATCH --mem-per-cpu={{mem_per_cpu}}
{%if node_list != None%}
#SBATCH --nodelist={{node_list}}
{%endif%}

{%if analysis_only == False%}
###Sequence preprocessing###

mothur '#set.current(processors={{processors}}); \
make.contigs(file={{job_name}}.files); \
summary.seqs(fasta=current); \
screen.seqs(fasta=current, contigsreport={{job_name}}.contigs.report, group=current, maxambig={{max_ambig}}, maxhomop={{max_homop}}, minlength={{min_length}}, maxlength={{max_length}}, minoverlap={{min_overlap}}); \
summary.seqs(fasta=current); \
unique.seqs(fasta=current); \
count.seqs(name=current, group=current); \
summary.seqs(fasta=current, count=current); \
align.seqs(fasta=current, reference={{align_database}}); \
summary.seqs(fasta=current, count=current); \
screen.seqs(fasta=current, count=current, summary=current,  optimize=start-end, criteria={{screen_criteria}}); \
summary.seqs(fasta=current, count=current); \
filter.seqs(fasta=current, vertical=T, trump=.); \
unique.seqs(fasta=current, count=current); \
summary.seqs(fasta=current, count=current); \
pre.cluster(fasta=current, count=current, diffs={{precluster_diffs}}); \
chimera.uchime(fasta=current, count=current, dereplicate={{chimera_dereplicate}}); \
remove.seqs(fasta=current, accnos=current); \
summary.seqs(fasta=current, count=current); \
classify.seqs(fasta=current, count=current, reference={{align_database}}, \
taxonomy={{taxonomy_database}}, cutoff={{classify_seqs_cutoff}}); \
remove.lineage(fasta=current, count=current, taxonomy=current, taxon=Chloroplast-Mitochondria-Eukaryota-unknown-Unknown);\
{%if mock == True%}

#Mock community analysis

remove.groups(fasta=current, count=current, taxonomy=current, groups=Mock); \
cluster.split(fasta=current, count=current, taxonomy=current, splitmethod=classify, taxlevel=4, cutoff={{cluster_cutoff}}); \
make.shared(list=current, count=current, label={{label}}); \
classify.otu(list=current, count=current, taxonomy=current, label={{label}}); \
count.groups(shared=current); phylotype(taxonomy=current); \
make.shared(list=current, count=current, label=1); \
classify.otu(list=current, count=current, taxonomy=current, label=1); \
system(cp zury_V3_V4.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.fasta mock.fasta); \
system(cp zury_V3_V4.trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.pick.pick.count_table mock.count_table); \
get.groups(fasta=mock.fasta, count=mock.count_table, groups=Mock); \
seq.error(fasta=current, count=current, reference=HMP_MOCK.v35.fasta, aligned=F); \
dist.seqs(fasta=current, cutoff=0.20); \
cluster(column=current, count=current); \
make.shared(list=current, count=current, label={{label}}); \
rarefaction.single(shared=current)\
{%else%}


#OTU clustering

cluster.split(fasta=current, count=current, taxonomy=current, splitmethod=classify, taxlevel=4, cutoff={{cluster_cutoff}}); \
make.shared(list=current, count=current, label={{label}}); \
classify.otu(list=current, count=current, taxonomy=current, label={{label}}); \
count.groups(shared=current); phylotype(taxonomy=current); \


#Phylotype

make.shared(list=current, count=current, label=1); \
classify.otu(list=current, count=current, taxonomy=current, label=1)'\
{%endif%}
{%else%}

###OTU approach analysis###

#Create directories and shorten shared file name

mkdir -p ./analysis/OTU/alpha ./analysis/OTU/beta
cp *list.shared ./analysis/OTU/{{job_name}}.shared
cp *{{label}}.cons.tax.summary ./analysis/OTU/alpha/{{job_name}}.tax.summary

#Go to subdirectory and subsample shared file

cd ./analysis/OTU
mothur '#set.current(processors={{processors}}, shared={{job_name}}.shared); sub.sample(shared=current)'

#Copy non-subsampled shared file to alpha directory and subsampled shared file to beta directory

cp {{job_name}}.shared ./alpha
cp {{job_name}}.{{label}}.subsample.shared ./beta

#Go to alpha directory and create krona chart, rarefaction, summary table

cd ./alpha
mothur_krona_XML.py {{job_name}}.tax.summary > {{job_name}}.krona.xml
ktImportXML {{job_name}}.krona.xml -o {{job_name}}.krona.html
mothur '#set.current(processors={{processors}}, shared={{job_name}}.shared); rarefaction.single(shared=current, calc=sobs, freq=100); summary.single(shared=current, calc=nseqs-coverage-sobs-invsimpson-shannon)'
../../../{{msc_path}} --rarefaction {{job_name}}.groups.rarefaction

#Go to beta directory and create dist files for Jaccard and YC measures

cd ../beta
mothur '#set.current(processors={{processors}}, shared={{job_name}}.{{label}}.subsample.shared); dist.shared(shared=current, calc=thetayc-jclass, output=square)'

#Create phylogenetic tree for Jaccard and YC measures

mothur '#tree.shared(phylip={{job_name}}.{{label}}.subsample.jclass.{{label}}.square.dist); tree.shared(phylip={{job_name}}.{{label}}.subsample.thetayc.{{label}}.square.dist)'

#Create scatter plots upon NMDS for Jaccard and YC measures

mothur '#nmds(phylip={{job_name}}.{{label}}.subsample.jclass.{{label}}.square.dist); nmds(phylip={{job_name}}.{{label}}.subsample.thetayc.{{label}}.square.dist)'

#Draw beta directory pictures for Jaccard and YC measures

../../../{{msc_path}} --phylip {{job_name}}.{{label}}.subsample.jclass.{{label}}.square.dist --tree {{job_name}}.{{label}}.subsample.jclass.{{label}}.square.tre --axes {{job_name}}.{{label}}.subsample.jclass.{{label}}.square.nmds.axes
../../../{{msc_path}} --phylip {{job_name}}.{{label}}.subsample.thetayc.{{label}}.square.dist --tree {{job_name}}.{{label}}.subsample.thetayc.{{label}}.square.tre --axes {{job_name}}.{{label}}.subsample.thetayc.{{label}}.square.nmds.axes
{%endif%}"""

    templ_str_its = """#!/bin/bash\

#SBATCH --job-name="{{job_name}}"\
#SBATCH --partition={{partition}}\
#SBATCH --nodes={{nodes}}\
#SBATCH --ntasks-per-node={{ntasks_per_node}}\
#SBATCH --mem-per-cpu={{mem_per_cpu}}\
{%if node_list != None%}
#SBATCH --nodelist={{node_list}}
{%endif%}
###Sequence preprocessing###

mothur '#set.current(processors={{processors}}); \ make.contigs(file={{job_name}}.files); \
summary.seqs(fasta=current); \
screen.seqs(fasta=current, contigsreport={{job_name}}.contigs.report, group=current, maxambig={{max_ambig}}, maxhomop={{max_homop}}, minlength={{min_length}}, maxlength={{max_length}}, minoverlap={{min_overlap}}); \
summary.seqs(fasta=current); \
chop.seqs(fasta=current, group=current, numbases={{chop_length}}); \
unique.seqs(fasta=current); \
count.seqs(name=current, group=current); \
summary.seqs(fasta=current, count=current); \
pre.cluster(fasta=current, count=current, diffs={{precluster_diffs}}); \
chimera.uchime(fasta=current, count=current, dereplicate={{chimera_dereplicate}}); \
remove.seqs(fasta=current, accnos=current); summary.seqs(fasta=current, count=current); \
classify.seqs(fasta=current, count=current,template={{align_database}}, taxonomy={{taxonomy_database}}, method=knn, search=blast, match=2, mismatch=-2, gapopen=-2, gapextend=-1, numwanted=1); \
remove.lineage(fasta=current, count=current, taxonomy=current, taxon=Chloroplast-Mitochondria-unknown-Unknown);\
{%if mock == True%}\

#Mock community analysis

remove.groups(fasta=current, count=current, taxonomy=current, groups=Mock); \
pariwise.seqs(fasta=current, cutoff={{cluster_cutoff}}); \
make.shared(list=current, count=current, label={{label}}); \
classify.otu(list=current, count=current, taxonomy=current, label={{label}}); \
count.groups(shared=current); phylotype(taxonomy=current); \
make.shared(list=current, count=current, label=1); \
classify.otu(list=current, count=current, taxonomy=current, label=1); \
system(cp zury_V3_V4.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.fasta mock.fasta); \
system(cp zury_V3_V4.trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.pick.pick.count_table mock.count_table); \
get.groups(fasta=mock.fasta, count=mock.count_table, groups=Mock); \
seq.error(fasta=current, count=current, reference=HMP_MOCK.v35.fasta, aligned=F); \
pariwise.seqs(fasta=current, cutoff={{cluster_cutoff}}); \
make.shared(list=current, count=current, label={{label}}); \
rarefaction.single(shared=current)\
{%else%}
pariwise.seqs(fasta=current, cutoff={{cluster_cutoff}}); \
make.shared(list=current, count=current, label={{label}}); \
classify.otu(list=current, count=current, taxonomy=current, label={{label}}); \
count.groups(shared=current); \
phylotype(taxonomy=current); \
make.shared(list=current, count=current, label=1); \
classify.otu(list=current, count=current, taxonomy=current, label=1)\
{%endif%}"""

    parser = argparse.ArgumentParser(description = "creates headnode-suitable\
                                                    mothur script",
                                     version = "0.9.1")
    database = parser.add_argument_group("database download options")
    headnode = parser.add_argument_group("headnode options")
    mothur = parser.add_argument_group("mothur options")
    draw = parser.add_argument_group("drawing options")
    parser.add_argument("-o",
                        "--output",
                        action = "store",
                        dest = "output_file_name",
                        metavar = "",
                        default = "mothur.sh",
                        help = "output file name. Default <mothur.sh>.")
    parser.add_argument("-n",
                        "--job-name",
                        action = "store",
                        dest = "job_name",
                        metavar = "",
                        default = "mothur.job",
                        help = "job name. MUST be same as <name>.files.\
                                Default <mothur>.")
    parser.add_argument("-m",
                        "--mock",
                        action = "store_true",
                        dest = "mock",
                        default = False,
                        help = "use if you have mock community group and\
                                want to calculate sequencing errors, classify\
                                mock OTUs and draw mock rarefaction curve.")
    parser.add_argument("-r",
                        "--run",
                        action = "store",
                        dest = "run",
                        metavar = "",
                        default = None,
                        help = "shell call. Use if you want to run the mothur\
                                script immediately. eg -r sh for regular bash\
                                or -r sbatch for slurm.")
    parser.add_argument("--analysis-only",
                        action = "store_true",
                        dest = "analysis_only",
                        default = False,
                        help = "outputs just the part involved in statistical\
                                analysis and drawing.")
    parser.add_argument("-t",
                        "--template",
                        action = "store",
                        dest = "template_file_name",
                        metavar = "",
                        default = None,
                        help = "path/to/template. Use if you want to use other\
                                template than default.")
    database.add_argument("--unite-ITS-02",
                          action = "store",
                          dest = "unite_ITS_02",
                          metavar = "",
                          default = None,
                          help = "path/to/download-database. Use if you want to\
                                  download UNITE ITS 02 database.")
    database.add_argument("--unite-ITS-s-02",
                          action = "store",
                          dest = "unite_ITS_s_02",
                          metavar = "",
                          default = None,
                          help = "path/to/download-database. Use if you want to\
                                  download UNITE ITS s 02 database.")
    database.add_argument("--silva-102",
                          action = "store",
                          dest = "silva_102",
                          metavar = "",
                          default = None,
                          help = "path/to/download-database. Use if you want to\
                                  download Silva v102.")
    database.add_argument("--silva-119",
                          action = "store",
                          dest = "silva_119",
                          metavar = "",
                          default = None,
                          help = "path/to/download-database. Use if you want to\
                                  download Silva v119.")
    database.add_argument("--silva-123",
                          action = "store",
                          dest = "silva_123",
                          metavar = "",
                          default = None,
                          help = "path/to/download-database. Use if you want to\
                                  download Silva v123.")
    headnode.add_argument("--partition",
                          action = "store",
                          dest = "partition",
                          metavar = "",
                          default = "long",
                          help = "headnode's partition. Values: test, short, big,\
                                  long, accel. Accel necessary for phi/gpu nodes\
                                  Default <long>.")
    headnode.add_argument("--nodes",
                          action = "store",
                          dest = "nodes",
                          metavar = "",
                          default = 1,
                          help = "number of nodes. Default: <1>.")
    headnode.add_argument("--ntasks-per-node",
                          action = "store",
                          dest = "ntasks_per_node",
                          metavar = "",
                          default = 6,
                          help = "number of tasks to invoke on each node.\
                                  Default <6>")
    headnode.add_argument("--mem-per-cpu",
                          action = "store",
                          dest = "mem_per_cpu",
                          metavar = "",
                          default = 24,
                          help = "maximum amount of real memory per node in\
                                  gigabytes. Default <24>.")
    headnode.add_argument("--node-list",
                          action = "store",
                          dest = "node_list",
                          metavar = "",
                          default = None,
                          help = "request a specific list of nodes")
    headnode.add_argument("--processors",
                          action = "store",
                          dest = "processors",
                          metavar = "",
                          default = 12,
                          help = "number of logical processors. Default: <12>")
    mothur.add_argument("--max-ambig",
                        action = "store",
                        dest = "max_ambig",
                        metavar = "",
                        default = 0,
                        help = "maximum number of ambiguous bases allowed.\
                                screen.seqs param. Default <0>.")
    mothur.add_argument("--max-homop",
                        action = "store",
                        dest = "max_homop",
                        metavar = "",
                        default = 8,
                        help = "maximum number of homopolymers allowed.\
                                screen.seqs param. Default <8>.")
    mothur.add_argument("--min-length",
                        action = "store",
                        dest = "min_length",
                        metavar = "",
                        default = 400,
                        help = "minimum length of read allowed.\
                                screen.seqs param. Default <400>.")
    mothur.add_argument("--max-length",
                        action = "store",
                        dest = "max_length",
                        metavar = "",
                        default = 500,
                        help = "minimum length of read allowed.\
                                screen.seqs param. Default <500>.")
    mothur.add_argument("--min-overlap",
                        action = "store",
                        dest = "min_overlap",
                        metavar = "",
                        default = 25,
                        help = "minimum number of bases overlap in contig.\
                                screen.seqs param. Default <25>.")
    mothur.add_argument("--screen-criteria",
                        action = "store",
                        dest = "screen_criteria",
                        metavar = "",
                        default = 95,
                        help = "trim start and end of read to fit this\
                                percentage of all reads.\
                                screen.seqs param. Default <95>.")
    mothur.add_argument("--chop-length",
                        action = "store",
                        dest = "chop_length",
                        metavar = "",
                        default = 250,
                        help = "cut all the reads to this length. Keeps front\
                                of the sequences. chop.seqs argument.\
                                Default <250>")
    mothur.add_argument("--precluster-diffs",
                        action = "store",
                        dest = "precluster_diffs",
                        metavar = "",
                        default = 4,
                        help = "number of differences between reads treated as\
                                insignificant. screen.seqs param. Default <4>.")
    mothur.add_argument("--chimera-dereplicate",
                        action = "store",
                        dest = "chimera_dereplicate",
                        metavar = "",
                        default = "T",
                        help = "checking for chimeras by group. chimera.uchime\
                                param. Default <T>.")
    mothur.add_argument("--classify-seqs-cutoff",
                        action = "store",
                        dest = "classify_seqs_cutoff",
                        metavar = "",
                        default = 80,
                        help = "bootstrap value for taxonomic assignment.\
                                classify.seqs param. Default <80>.")
    mothur.add_argument("--classify-ITS",
                        action = "store_true",
                        dest = "classify_ITS",
                        default = False,
                        help = "removes align.seqs step and modifies\
                                classify.seqs with <method=knn>,\
                                                   <search=blast>,\
                                                   <match=2>,\
                                                   <mismatch=-2>,\
                                                   <gapopen=-2>,\
                                                   <gapextend=-1>,\
                                                   <numwanted=1>).\
                                Default <False>")
    mothur.add_argument("--align-database",
                        action = "store",
                        dest = "align_database",
                        metavar = "",
                        default = "~/db/Silva.nr_v119/silva.nr_v119.align",
                        help = "path/to/align-database. Used by align.seqs\
                                command as <reference> argument. Default\
                                <~/db/Silva.nr_v119/silva.nr_v119.align>.")
    mothur.add_argument("--taxonomy-database",
                        action = "store",
                        dest = "taxonomy_database",
                        metavar = "",
                        default = "~/db/Silva.nr_v119/silva.nr_v119.tax",
                        help = "path/to/taxonomy-database. Used by\
                                classify.seqs as <taxonomy> argument.\
                                Default <~/db/Silva.nr_v119/silva.nr_v119.tax>")
    mothur.add_argument("--cluster-cutoff",
                        action = "store",
                        dest = "cluster_cutoff",
                        metavar = "",
                        default = 0.15,
                        help = "cutoff value. Smaller == faster cluster param.\
                                Default <0.15>.")
    mothur.add_argument("--label",
                        action = "store",
                        dest = "label",
                        metavar = "",
                        default = 0.03,
                        help = "label argument for number of commands for OTU\
                                analysis approach. Default 0.03.")
    draw.add_argument("--rarefaction",
                      action = "store",
                      dest = "rarefaction",
                      metavar = "",
                      help = "path/to/rarefaction-file. Use to draw rarefaction\
                              curves plot.")
    draw.add_argument("--phylip",
                      action = "store",
                      dest = "phylip",
                      metavar = "",
                      help = "path/to/phylip-file. Use to draw heatmap and\
                              tree.")
    draw.add_argument("--tree",
                      action = "store",
                      metavar = "",
                      help = "path/to/tree-file. Use to draw dendrogram.")
    draw.add_argument("--axes",
                      action = "store",
                      dest = "axes",
                      metavar = "",
                      help = "path/to/axes-file. Use to draw scatter plots.")
    args = parser.parse_args()

    if args.unite_ITS_02 != None:
        download_path = "{0}/Unite_ITS_02.zip".format(args.unite_ITS_02)
        print "Downloading to {0}".format(download_path)
        get_db("https://www.mothur.org/w/images/4/49/Unite_ITS_02.zip",
               download_path)
        print "Downloading done!"
        print "Unpacking..."
        try:
            os.system("unzip {0}".format(download_path))
            os.system("rm {0}".format(download_path))
            print "Unpacking done!"
        except:
            print "Failed to extract file... skipping"
    else:
        pass
    if args.unite_ITS_s_02 != None:
        download_path = "{0}/Unite_ITS_s_02.zip".format(args.Unite_ITS_s_02)
        print "Downloading to {0}/Unite_ITS_s_02.zip".format(args.Unite_ITS_s_02)
        get_db("https://www.mothur.org/w/images/2/27/Unite_ITS_s_02.zip",
               download_path)
        print "Downloading done!"
        print "Unpacking..."
        try:
            os.system("unzip {0}".format(download_path))
            os.system("rm {0}".format(download_path))
            print "Failed to extract file... skipping"
        except:
            print "Unpacking done!"
    else:
        pass
    if args.silva_102 != None:
        download_path = "{0}/Silva.bacteria.zip".format(args.silva_102)
        print "Downloading to {0}/Silva.bacteria.zip".format(args.silva_102)
        get_db("https://www.mothur.org/w/images/9/98/Silva.bacteria.zip",
               download_path)
        print "Downloading done!"
        print "Unpacking..."
        try:
            os.system("unzip {0}".format(download_path))
            os.system("rm {0}".format(download_path))
            print "Unpacking done!"
        except:
            print "Failed to extract file... skipping"
        download_path = "{0}/Silva.archaea.zip".format(args.silva_102)
        print "Downloading to {0}/Silva.archaea.zip".format(args.silva_102)
        get_db("https://www.mothur.org/w/images/3/3c/Silva.archaea.zip",
               download_path)
        print "Downloading done!"
        print "Unpacking..."
        try:
            os.system("unzip {0}".format(download_path))
            os.system("rm {0}".format(download_path))
            print "Unpacking done!"
        except:
            print "Failed to extract file... skipping"
        download_path = "{0}/Silva.eukarya.zip".format(args.silva_102)
        print "Downloading to {0}/Silva.eukarya.zip".format(args.silva_102)
        get_db("https://www.mothur.org/w/images/1/1a/Silva.eukarya.zip",
               download_path)
        print "Downloading done!"
        print "Unpacking..."
        try:
            os.system("unzip {0}".format(download_path))
            os.system("rm {0}".format(download_path))
            print "Unpacking done!"
        except:
            print "Failed to extract file... skipping"
    else:
        pass
    if args.silva_119 != None:
        download_path = "{0}/Silva.nr_v119.tgz".format(args.silva_119)
        print "Downloading to {0}/Silva.nr_v119.tgz".format(args.silva_119)
        get_db("http://www.mothur.org/w/images/2/27/Silva.nr_v119.tgz",
               download_path)
        print "Downloading done!"
        print "Unpacking..."
        try:
            os.mkdir("{0}/Silva.nr_v119".format(args.silva_119))
            os.system("tar -xf {0} --directory {1}".format(download_path,
                                                           "{0}/Silva.nr_v119".format(args.silva_119)))
            os.system("rm {0}".format(download_path))
            print "Unpacking done!"
        except:
            print "Failed to extract file... skipping"
    else:
        pass
    if args.silva_123 != None:
        download_path = "{0}/Silva.nr_v123.tgz".format(args.silva_123)
        print "Downloading to {0}/Silva.nr_v123.tgz".format(args.silva_123)
        get_db("https://www.mothur.org/w/images/b/be/Silva.nr_v123.tgz",
               download_path)
        print "Downloading done!"
        print "Unpacking..."
        try:
            os.mkdir("{0}/Silva.nr_v119".format(args.silva_119))
            os.system("tar -xf {0} --directory {1}".format(download_path,
                                                           "{0}/Silva.nr_v119".format(args.silva_119)))
            os.system("rm {0}".format(download_path))
            print "Unpacking done!"
        except:
            print "Failed to extract file... skipping"
    if args.rarefaction or args.phylip or args.tree or args.axes != None:
        if args.rarefaction != None:
            draw_rarefaction(args.rarefaction)
        else:
            pass
        if args.phylip != None:
            draw_heatmap(args.phylip)
        else:
            pass
        if args.tree != None:
            draw_tree(args.tree)
        else:
            pass
        if args.axes != None:
            draw_scatter(args.axes)
        else:
            pass
    else:
        if args.template_file_name != None:
            loaded_template = load_template(args.template_file_name)
        else:
            if args.classify_ITS == True:
                loaded_template = load_template_str(templ_str_its)
            else:
                loaded_template = load_template_str(templ_str_otu)
        rendered_template = render_template(loaded_template,
                                            job_name = args.job_name,
                                            mock = args.mock,
                                            analysis_only = args.analysis_only,
                                            partition = args.partition,
                                            nodes = args.nodes,
                                            ntasks_per_node = args.ntasks_per_node,
                                            mem_per_cpu = args.mem_per_cpu,
                                            node_list = args.node_list,
                                            processors = args.processors,
                                            max_ambig = args.max_ambig,
                                            max_homop = args.max_homop,
                                            min_length = args.min_length,
                                            max_length = args.max_length,
                                            min_overlap = args.min_overlap,
                                            screen_criteria = args.screen_criteria,
                                            chop_length = args.chop_length,
                                            precluster_diffs = args.precluster_diffs,
                                            chimera_dereplicate = args.chimera_dereplicate,
                                            classify_seqs_cutoff = args.classify_seqs_cutoff,
                                            align_database = args.align_database,
                                            taxonomy_database = args.taxonomy_database,
                                            cluster_cutoff = args.cluster_cutoff,
                                            label = args.label)
        save_template(args.output_file_name,
                      rendered_template)
        if args.run != None:
            os.system("{0} {1}".format(args.run, args.output_file_name))
        else:
            pass
if __name__ == "__main__":
    main()
