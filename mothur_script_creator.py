#! /usr/bin/env python

import jinja2 as jj2
import argparse


def load_template(template_file):
    template_Loader = jj2.FileSystemLoader(searchpath = ".")
    template_Env = jj2.Environment(loader = template_Loader)
    template = template_Env.get_template(template_file)
    return template


def render_template(template_loaded,
                    job_name,
                    mock,
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
    parser = argparse.ArgumentParser(description = "creates headnode-suitable\
                                                    mothur script",
                                     version = "tests")
    parser.add_argument(action = "store",
                        dest = "template_file_name",
                        metavar = "path/to/template",
                        help = "template directory path.")
    parser.add_argument("-o",
                        "--output",
                        action = "store",
                        dest = "output_file_name",
                        metavar = "",
                        default = "mothur.sh",
                        help = "output file name. Default <mothur.sh>")
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
                                mock OTUs and draw mock rarefaction curve")
    args = parser.parse_args()

    loaded_template = load_template(args.template_file_name)
    rendered_template = render_template(loaded_template,
                                        args.job_name,
                                        args.mock)
    save_template(args.output_file_name,
                  rendered_template)

if __name__ == "__main__":
    main()
