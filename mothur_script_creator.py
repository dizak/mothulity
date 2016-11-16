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
                    screen_criteria,
                    precluster_diffs = 4,
                    chimera_dereplicate = "T"):
    mem_per_cpu = "{0}G".format(mem_per_cpu)
    template_vars = {"job_name": job_name,
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
                     "chimera_dereplicate": chimera_dereplicate}
    template_rendered = template_loaded.render(template_vars)
    return template_rendered


def save_template(out_file_name):
    with open("{0}.html".format(out_file_name), "w") as fout:
        fout.write(template_rendered)


def main():
    parser = argparse.ArgumentParser(description = "creates headnode-suitable\
                                                    mothur script",
                                     version = "tests")
    parser.add_argument("--input",
                        required = True,
                        help = "specifies template file")
    parser.add_argument("--job-name",
                        required = True,
                        help = "specifies job name")
    parser.add_argument("--output",
                        required = True,
                        help = "specifies output file name")
    args = parser.parse_args()

    loaded_template = load_template(args.input)
    rendered_template = render_template(loaded_template)
    save_template(args.output)

if __name__ == "__main__":
    main()
