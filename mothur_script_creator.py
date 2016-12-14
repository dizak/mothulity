#! /usr/bin/env python

import jinja2 as jj2
import argparse
import os

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
                    precluster_diffs = 4,
                    chimera_dereplicate = "T",
                    classify_seqs_cutoff = 80,
                    align_database = None,
                    taxonomy_database = None,
                    cluster_cutoff = 0.15):
    mem_per_cpu = "{0}G".format(mem_per_cpu)
    template_vars = {"job_name": job_name,
                     "mock": mock,
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
                     "precluster_diffs": precluster_diffs,
                     "chimera_dereplicate": chimera_dereplicate,
                     "classify_seqs_cutoff": classify_seqs_cutoff,
                     "align_database": align_database,
                     "taxonomy_database": taxonomy_database,
                     "cluster_cutoff": cluster_cutoff}
    template_rendered = template_loaded.render(template_vars)
    return template_rendered


def save_template(out_file_name,
                  template_rendered):
    with open(out_file_name, "w") as fout:
        fout.write(template_rendered)


def main():
    templ_str = """#!/bin/bash\n\n#SBATCH --job-name="{{job_name}}"\n#SBATCH --partition={{partition}}\n#SBATCH --nodes={{nodes}}\n#SBATCH --ntasks-per-node={{ntasks_per_node}}\n#SBATCH --mem-per-cpu={{mem_per_cpu}}\n{%if node_list != None%}#SBATCH --nodelist={{node_list}}{%endif%}\n\nmothur '#set.current(processors={{processors}}); make.contigs(file={{job_name}}.files); summary.seqs(fasta=current); screen.seqs(fasta=current, contigsreport={{job_name}}.contigs.report, group=current, maxambig={{max_ambig}}, maxhomop={{max_homop}}, minlength={{min_length}}, maxlength={{max_length}}, minoverlap={{min_overlap}}); summary.seqs(fasta=current); unique.seqs(fasta=current); count.seqs(name=current, group=current); summary.seqs(fasta=current, count=current); align.seqs(fasta=current, reference={{align_database}}); summary.seqs(fasta=current, count=current); screen.seqs(fasta=current, count=current, summary=current,  optimize=start-end, criteria={{screen_criteria}}); summary.seqs(fasta=current, count=current); filter.seqs(fasta=current, vertical=T, trump=.); unique.seqs(fasta=current, count=current); summary.seqs(fasta=current, count=current); pre.cluster(fasta=current, count=current, diffs={{precluster_diffs}}); chimera.uchime(fasta=current, count=current, dereplicate={{chimera_dereplicate}}); remove.seqs(fasta=current, accnos=current); summary.seqs(fasta=current, count=current); classify.seqs(fasta=current, count=current, reference={{align_database}}, taxonomy={{taxonomy_database}}, cutoff={{classify_seqs_cutoff}}); remove.lineage(fasta=current, count=current, taxonomy=current, taxon=Chloroplast-Mitochondria-Eukaryota-unknown-Unknown);{%if mock == True%} remove.groups(fasta=current, count=current, taxonomy=current, groups=Mock); cluster.split(fasta=current, count=current, taxonomy=current, splitmethod=classify, taxlevel=4, cutoff={{cluster_cutoff}}); make.shared(list=current, count=current, label=0.03); classify.otu(list=current, count=current, taxonomy=current, label=0.03); count.groups(shared=current); phylotype(taxonomy=current); make.shared(list=current, count=current, label=1); classify.otu(list=current, count=current, taxonomy=current, label=1); system(cp zury_V3_V4.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.fasta mock.fasta); system(cp zury_V3_V4.trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.pick.pick.count_table mock.count_table); get.groups(fasta=mock.fasta, count=mock.count_table, groups=Mock); seq.error(fasta=current, count=current, reference=HMP_MOCK.v35.fasta, aligned=F); dist.seqs(fasta=current, cutoff=0.20); cluster(column=current, count=current); make.shared(list=current, count=current, label=0.03); rarefaction.single(shared=current){%else%}cluster.split(fasta=current, count=current, taxonomy=current, splitmethod=classify, taxlevel=4, cutoff={{cluster_cutoff}}); make.shared(list=current, count=current, label=0.03); classify.otu(list=current, count=current, taxonomy=current, label=0.03); count.groups(shared=current); phylotype(taxonomy=current); make.shared(list=current, count=current, label=1); classify.otu(list=current, count=current, taxonomy=current, label=1){%endif%}'"""

    parser = argparse.ArgumentParser(description = "creates headnode-suitable\
                                                    mothur script",
                                     version = "tests")
    headnode = parser.add_argument_group("headnode options")
    mothur = parser.add_argument_group("mothur options")
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
                        action = "store_true",
                        dest = "run",
                        default = False,
                        help = "use if you want to run the mothur script\
                                immediately. Default <False>.")
    parser.add_argument("-t",
                        "--template",
                        action = "store",
                        dest = "template_file_name",
                        metavar = "",
                        default = None,
                        help = "path/to/template. Use if you want to use other\
                                template than default.")
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
                          help = "number of tasks to invoke on each node")
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
    mothur.add_argument("--precluster-diffs",
                        action = "store",
                        dest = "precluster_diffs",
                        metavar = "",
                        default = 4,
                        help = "number of differences between reads treated as\
                                insignificant. screen.seqs param. Default <25>.")
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
    mothur.add_argument("--align-database",
                        required = True,
                        action = "store",
                        dest = "align_database",
                        metavar = "",
                        help = "path/to/align-database. Used by align.seqs\
                                command as <reference> argument. Required.")
    mothur.add_argument("--taxonomy-database",
                        action = "store",
                        dest = "taxonomy_database",
                        metavar = "",
                        help = "path/to/taxonomy-database. Used by\
                                classify.seqs as <taxonomy> argument.\
                                Required")
    mothur.add_argument("--cluster-cutoff",
                        action = "store",
                        dest = "cluster_cutoff",
                        metavar = "",
                        default = 0.15,
                        help = "cutoff value. Smaller == faster cluster param.\
                                Default <0.15>.")
    args = parser.parse_args()

    if args.template_file_name != None:
        loaded_template = load_template(args.template_file_name)
    else:
        loaded_template = load_template_str(templ_str)
    rendered_template = render_template(loaded_template,
                                        job_name = args.job_name,
                                        mock = args.mock,
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
                                        precluster_diffs = args.precluster_diffs,
                                        chimera_dereplicate = args.chimera_dereplicate,
                                        classify_seqs_cutoff = args.classify_seqs_cutoff,
                                        align_database = args.align_database,
                                        taxonomy_database = args.database,
                                        cluster_cutoff = args.cluster_cutoff)
    save_template(args.output_file_name,
                  rendered_template)
    if args.run == True:
        os.system("sbatch {0}".format(args.output_file_name))

if __name__ == "__main__":
    main()
