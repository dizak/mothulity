#! /usr/bin/env python

import jinja2 as jj2
import argparse


def load_template_str(template_str):
    template = jj2.Environment().from_string(template_str)
    return template


def load_template(template_file):
    template_Loader = jj2.FileSystemLoader(searchpath = ".")
    template_Env = jj2.Environment(loader = template_Loader)
    template = template_Env.get_template(template_file)
    return template


def render_template(template_loaded,
                    job_name,
                    mock,
                    partition,
                    nodes,
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
                     "cluster_cutoff": cluster_cutoff}
    template_rendered = template_loaded.render(template_vars)
    return template_rendered


def save_template(out_file_name,
                  template_rendered):
    with open(out_file_name, "w") as fout:
        fout.write(template_rendered)


def main():
    templ_str = """#!/bin/bash\n\n#SBATCH --job-name="{{job_name}}"\n#SBATCH --partition={{partition}}\n#SBATCH --nodes={{nodes}}\n#SBATCH --ntasks-per-node={{ntasks_per_node}}\n#SBATCH --mem-per-cpu={{mem_per_cpu}}\n{%if node_list != None%}#SBATCH --nodelist={{node_list}}{%endif%}\n\nmothur '#set.current(processors={{processors}}); make.contigs(file={{job_name}}.files); summary.seqs(fasta=current); screen.seqs(fasta=current, contigsreport={{job_name}}.contigs.report, group=current, maxambig={{max_ambig}}, maxhomop={{max_homop}}, minlength={{min_length}}, maxlength={{max_length}}, minoverlap={{min_overlap}}); summary.seqs(fasta=current); unique.seqs(fasta=current); count.seqs(name=current, group=current); summary.seqs(fasta=current, count=current); align.seqs(fasta=current, reference=/home/dizak/db/Silva.nr_v119/silva.nr_v119.align); summary.seqs(fasta=current, count=current); screen.seqs(fasta=current, count=current, summary=current,  optimize=start-end, criteria={{screen_criteria}}); summary.seqs(fasta=current, count=current); filter.seqs(fasta=current, vertical=T, trump=.); unique.seqs(fasta=current, count=current); summary.seqs(fasta=current, count=current); pre.cluster(fasta=current, count=current, diffs={{precluster_diffs}}); chimera.uchime(fasta=current, count=current, dereplicate={{chimera_dereplicate}}); remove.seqs(fasta=current, accnos=current); summary.seqs(fasta=current, count=current); classify.seqs(fasta=current, count=current, reference=/home/dizak/db/Silva.nr_v119/silva.nr_v119.align, taxonomy=/home/dizak/db/Silva.nr_v119/silva.nr_v119.tax, cutoff={{classify_seqs_cutoff}}); remove.lineage(fasta=current, count=current, taxonomy=current, taxon=Chloroplast-Mitochondria-Eukaryota-unknown-Unknown);{%if mock == True%} remove.groups(fasta=current, count=current, taxonomy=current, groups=Mock); cluster.split(fasta=current, count=current, taxonomy=current, splitmethod=classify, taxlevel=4, cutoff={{cluster_cutoff}}); make.shared(list=current, count=current, label=0.03); classify.otu(list=current, count=current, taxonomy=current, label=0.03); count.groups(shared=current); phylotype(taxonomy=current); make.shared(list=current, count=current, label=1); classify.otu(list=current, count=current, taxonomy=current, label=1); system(cp zury_V3_V4.trim.contigs.good.unique.good.filter.unique.precluster.pick.pick.fasta mock.fasta); system(cp zury_V3_V4.trim.contigs.good.unique.good.filter.unique.precluster.denovo.uchime.pick.pick.count_table mock.count_table); get.groups(fasta=mock.fasta, count=mock.count_table, groups=Mock); seq.error(fasta=current, count=current, reference=HMP_MOCK.v35.fasta, aligned=F); dist.seqs(fasta=current, cutoff=0.20); cluster(column=current, count=current); make.shared(list=current, count=current, label=0.03); rarefaction.single(shared=current){%else%}cluster.split(fasta=current, count=current, taxonomy=current, splitmethod=classify, taxlevel=4, cutoff={{cluster_cutoff}}); make.shared(list=current, count=current, label=0.03); classify.otu(list=current, count=current, taxonomy=current, label=0.03); count.groups(shared=current); phylotype(taxonomy=current); make.shared(list=current, count=current, label=1); classify.otu(list=current, count=current, taxonomy=current, label=1){%endif%}'"""

    parser = argparse.ArgumentParser(description = "creates headnode-suitable\
                                                    mothur script",
                                     version = "tests")
    parser.add_argument("-o",
                        "--output",
                        action = "store",
                        dest = "output_file_name",
                        metavar = "",
                        default = "mothur.sh",
                        help = "output file name. Default <mothur.sh>")
    parser.add_argument("-j",
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
                                mock OTUs and draw mock rarefaction curve")
    parser.add_argument("-p",
                        "--partition",
                        action = "store",
                        dest = "partition",
                        metavar = "",
                        default = "long",
                        help = "headnode's partition. Values: test, short, big,\
                                long, accel. Accel necessary for phi/gpu nodes\
                                Default <long>.")
    parser.add_argument("-n",
                        "--nodes",
                        action = store,
                        dest = nodes,
                        metavar = "",
                        default = 1,
                        help = "headnode's nodes number. Default: <1>.")
    parser.add_argument("--ntasks-per-node",
                        action = "store",
                        dest = "ntask_per_node",
                        metavar = "",
                        default = 6,
                        help = "number of tasks to invoke on each headnode's\
                                node")
    parser.add_argument("-t",
                        "--template",
                        action = "store",
                        dest = "template_file_name",
                        metavar = "path/to/template",
                        default = None,
                        help = "use if you want to use other template than\
                                default")
    args = parser.parse_args()

    if args.template_file_name != None:
        loaded_template = load_template(args.template_file_name)
    else:
        loaded_template = load_template_str(templ_str)
    rendered_template = render_template(loaded_template,
                                        args.job_name,
                                        args.mock,
                                        args.partition)
    save_template(args.output_file_name,
                  rendered_template)

if __name__ == "__main__":
    main()
