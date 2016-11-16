#! /usr/bin/env python

import jinja2 as jj2


def load_template(template_file):
    template_Loader = jj2.FileSystemLoader(searchpath = ".")
    template_Env = jj2.Environment(loader = template_Loader)
    template = template_Env.get_template(template_file)
    return template


def render_template(template_loaded):
    template_vars = {}
    template_rendered = template_loaded.render(template_vars)


def save_template(out_file_name):
    with open("{0}.html".format(out_file_name), "w") as fout:
        fout.write(template_rendered)


def main():
    pass

if __name__ == "__main__":
    main()
