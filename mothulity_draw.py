#! /usr/bin/env python


from utilities import get_dir_path
import os
import ConfigParser
import argparse
from Bio import Phylo as ph
import matplotlib
matplotlib.use('Agg')
import pylab
import matplotlib.pyplot as plt
import matplotlib.style as style
import mpld3
from pandas import read_csv
from seaborn import heatmap
from seaborn import pairplot
from seaborn import lmplot


__author__ = "Dariusz Izak IBB PAS"


def load_template_file(template_file):
    template_Loader = jj2.FileSystemLoader(searchpath="/")
    template_Env = jj2.Environment(loader=template_Loader)
    template = template_Env.get_template(template_file)
    return template


def render_template(template_loaded,
                    venn_diagrams,
                    javascript):
    template_vars = {"venn_diagrams": venn_diagrams}
    template_rendered = template_loaded.render(template_vars)
    return template_rendered


def save_template(out_file_name,
                  template_rendered):
    with open(out_file_name, "w") as fout:
        fout.write(template_rendered)


def draw_rarefaction(file_name):
    output_file = "{}.mpld3.html".format(file_name)
    df = read_csv(file_name,
                  sep="\t",
                  index_col="numsampled")
    cols = [i for i in df.columns if "lci" not in i]
    cols = [i for i in cols if "hci" not in i]
    df = df[cols]
    fig, ax = plt.subplots()
    df[cols].plot(ax=ax,
                  figsize=(15, 8))
    labels = list(df.columns.values)
    for i in range(len(labels)):
        tooltip = mpld3.plugins.LineLabelTooltip(ax.get_lines()[i],
                                                 labels[i])
        mpld3.plugins.connect(plt.gcf(), tooltip)
    plt.grid(True)
    plt.title("Rarefaction curve")
    plt.ylabel("OTU count")
    plt.xlabel("number of sequences")
    with open(output_file, "w") as fout:
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


def summary2html(file_name,
                 css_link,
                 js_file_name):
    with open(js_file_name) as fin:
        js_str = fin.read()
    output_file = "{}.html".format(file_name)
    df = read_csv(file_name, sep="\t")
    html_str = df.to_html(classes=["compact",
                                   "hover",
                                   "order-column"],
                          index=False)
    html_str = "{0}{1}{2}".format(css_link,
                                  html_str,
                                  js_str)
    with open(output_file, "w") as fout:
        fout.write(html_str)


def main():
    parser = argparse.ArgumentParser(prog="mothulity_draw",
                                     usage="mothulity_draw [OPTION]",
                                     description="draws plots from\
                                     mothur-generated files.",
                                     version="0.9.4")
    parser.add_argument(action="store",
                        dest="input_file_name",
                        metavar="path/to/input_file",
                        default=".",
                        help="input file name. Default CWD.")
    parser.add_argument("--output",
                        dest="output_file_name",
                        metavar="",
                        default=None,
                        help="output file name")
    parser.add_argument("--rarefaction",
                        action="store",
                        dest="rarefaction",
                        metavar="",
                        help="path/to/rarefaction-file. Use to draw rarefaction\
                        curves plot.")
    parser.add_argument("--phylip",
                        action="store",
                        dest="phylip",
                        metavar="",
                        help="path/to/phylip-file. Use to draw heatmap and\
                        tree.")
    parser.add_argument("--tree",
                        action="store",
                        dest="tree",
                        metavar="",
                        help="path/to/tree-file. Use to draw dendrogram.")
    parser.add_argument("--axes",
                        action="store",
                        dest="axes",
                        metavar="",
                        help="path/to/axes-file. Use to draw scatter plots.")
    parser.add_argument("--summary-table",
                        action="store",
                        dest="summary_table",
                        metavar="",
                        help="/path/to/summary-table. Use to convert summary\
                        table into fancy DataTable.")
    parser.add_argument("--render-html",
                        action="store_true",
                        dest="render_html",
                        default=False,
                        help="path/to/html-template-file. Use to pass args into\
                        fancy html.")
    args = parser.parse_args()

    config_path_abs = get_dir_path("mothulity.config")
    config = ConfigParser.SafeConfigParser()
    config.read(config_path_abs)

    if args.rarefaction is not None:
        draw_rarefaction(args.input_file_name)
    else:
        pass
    if args.phylip is not None:
        draw_heatmap(args.input_file_name)
    else:
        pass
    if args.tree is not None:
        draw_tree(args.input_file_name)
    else:
        pass
    if args.axes is not None:
        draw_scatter(args.input_file_name)
    else:
        pass
    if args.summary_table is not None:
        summary2html(args.input_file_name)
    else:
        pass


if __name__ == '__main__':
    main()
