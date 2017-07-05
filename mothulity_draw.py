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
from lxml import etree as et
import pandas as pd


__author__ = "Dariusz Izak IBB PAS"


def load_template_file(template_file):
    """
    Load jinja2 template file. Search path starts from root directory so no
    chroot.

    Parameters
    -------
    template_file: str
        Template file name.
    searchpath: str, default </>
        Root directory for template lookup.

    Returns
    -------
    jinja2.Template
    """
    template_Loader = jj2.FileSystemLoader(searchpath="/")
    template_Env = jj2.Environment(loader=template_Loader)
    template = template_Env.get_template(template_file)
    return template


def render_template(template_loaded,
                    venn_diagrams,
                    javascript):
    """
    Render jinja2.Template to unicode.

    Parameters
    -------
    loaded_template: jinj2.Template
        Template to render.

    Returns
    -------
    unicode
        Template content with passed variables.
    """
    template_vars = {"venn_diagrams": venn_diagrams}
    template_rendered = template_loaded.render(template_vars)
    return template_rendered


def save_template(output_file_name,
                  template_rendered):
    """
    Save rendered template to file.

    Parameters
    -------
    out_file_name: str
        Output file name.
    template_rendered: unicode
        Temlplate rendered to unicode object.
    """
    with open(output_file_name, "w") as fout:
        fout.write(template_rendered)


def draw_rarefaction(input_file_name,
                     output_file_name,
                     title="Rarefaction curve",
                     ylabel="OTU count",
                     xlabel="number of sequences",
                     index_col="numsampled",
                     figsize=(15, 8),
                     sep="\t"):
    """
    Draw rarefaction plot from mothur's rarefaction file and save figure to file.

    Parameters
     -------
    input_file_name: str
        Input file name.
    output_file_name: str
        Output file name.
    title: str, default <Rarefaction curve>
        Displayed plot title.
    ylabel: str, default <OTU count>
        Displayed label for y axis.
    xlabel: str, default <number of sequences>
        Displayed label for x axis.
    index_col: str or int, default <numsampleds>
        Index column name in shared file.
    figsize: tuple of int, default <(15, 8)>
        Size of figure to be saved.
    sep: str, default <\t>
        Delimiter to use for reading-in rarefaction file.
    """
    df = read_csv(input_file_name,
                  sep=sep,
                  index_col=index_col)
    cols = [i for i in df.columns if "lci" not in i]
    cols = [i for i in cols if "hci" not in i]
    df = df[cols]
    fig, ax = plt.subplots()
    df[cols].plot(ax=ax,
                  figsize=figsize)
    labels = list(df.columns.values)
    for i in range(len(labels)):
        tooltip = mpld3.plugins.LineLabelTooltip(ax.get_lines()[i],
                                                 labels[i])
        mpld3.plugins.connect(plt.gcf(), tooltip)
    plt.grid(True)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    with open(output_file_name, "w") as fout:
        fout.write(mpld3.fig_to_html(fig))


def draw_heatmap(input_file_name,
                 output_file_name,
                 sep="\t",
                 skiprows=1,
                 header=None,
                 index_col=0,
                 color_map="plasma"):
    """
    Draw heatmap from mothur's phylip file and save figure to file.

    Parameters
    -------
    input_file_name: str
        Input file name.
    output_file_name: str
        Output file name.
    sep: str, default <\t>
        Delimiter to use for reading-in rarefaction file.
    skiprows: int, default <1>
        Rows to skip when reading-in phylip file for proper parsing.
    header: int or None, default: <None>
        Row number to use as column names. None if there is not any.
    index_col: str or int, default <0>
        Index column name in shared file.
    color_map: str, default <plasma>
        Color map to use in the figure.
    """
    df = read_csv(input_file_name,
                  sep=sep,
                  skiprows=skiprows,
                  header=header,
                  index_col=index_col)
    df.columns = df.index
    fig = heatmap(df, square=True, cmap=color_map).get_figure()
    fig.savefig(output_file_name)


def draw_tree(input_file_name,
              output_file_name,
              tree_format="newick"):
    """
    Draw dendrogram from mothur's tre file and save figure to file.

    Parameters
    -------
    input_file_name: str
        Input file name.
    output_file_name: str
        Output file name.
    tree_format: str, default <newick>
        File format of dendrogram.
    """
    pylab.ion()
    tree = ph.read(input_file_name, tree_format)
    ph.draw(tree)
    pylab.savefig(output_file_name)


def draw_scatter(input_file_name,
                 output_file_name,
                 xlabel="axis1",
                 ylabel="axis2",
                 hue="group",
                 fit_reg=False,
                 sep="\t"):
    """
    Draw scatter plot from mothur's axes file and save figure to file.

    Parameters
    -------
    input_file_name: str
        Input file name.
    output_file_name: str
        Output file name.
    xlabel: str, default <axis1>
        Displayed label for x axis.
    ylabel: str, default <axis2>
        Displayed label for y axis.
    hue: str, default <group>
        Column name in axes file defining subset of data.
    fit_reg: bool, default <False>
        Draw regression line if <True>.
    sep: str, default <\t>
        Delimiter to use for reading-in axes file.
    """
    df = read_csv(input_file_name,
                  sep=sep)
    fig = lmplot(x=xlabel,
                 y=ylabel,
                 data=df,
                 hue=hue,
                 fit_reg=fit_reg)
    fig.savefig(output_file_name)


def summary2html(input_file_name,
                 output_file_name,
                 css_link,
                 js_input_file_name,
                 css_classes=["compact",
                              "hover",
                              "order-column"],
                 sep="\t"):
    """
    Convert raw mothur's summary table file into fancy HTML.

    Parameters
    -------
    input_file_name: str
        Input file name.
    output_file_name: str
        Output file name.
    css_link: str,
        HTML link tag with content, used for displaying summary table.
    js_input_file_name: str
        JavaScript file name for displaying summary table.
    css_classes: list of str, default: ["compact", "hover", "order-column"]
        CSS classes for displaying summary table.
    sep: str, default <\t>
        Delimiter to use for reading-in axes file.
    """
    with open(js_input_file_name) as fin:
        js_str = fin.read()
    df = read_csv(input_file_name, sep=sep)
    html_df = df.to_html(classes=css_classes,
                         index=False)
    html_str = "{0}{1}{2}".format(css_link,
                                  html_df,
                                  js_str)
    with open(output_file_name, "w") as fout:
        fout.write(html_str)


def get_daughter_df(df,
                    mother_taxon,
                    mother_rank,
                    tax_level):
    """
    Get pandas.DataFrame containing daughter taxa of passed mother taxon info.
    Based upon mothur's tax.summary file.

    Parameters:
    --------
    df: pandas.DataFrame
        pandas.DataFrame read from mothur's tax.summary file.
    mother_taxon: str
        Taxon of which daughter taxa will be in returned pandas.DataFrame.
    mother_rank: str
        Taxon rankID value of which daughter taxa will be in returned pandas.DataFrame.
    tax_level: int
        Taxon taxonomical level value of which daughter taxa will be in returned pandas.DataFrame.
    Returns
    -------
    pandas.DataFrame
        pandas.DataFrame containing daughter taxa.
    """
    sel_df = df[(df.taxon == mother_taxon) &
                (df.rankID == mother_rank) &
                (df.taxlevel == tax_level)]
    daughter_levels = int(sel_df.daughterlevels)
    if daughter_levels > 0:
        mother_rank = sel_df.rankID.to_string(index=False)
        daughter_df = df[df.rankID.str.contains(mother_rank)][df.rankID.str.len() == len(mother_rank) + 2]
        return daughter_df


def populate_node(df,
                  node,
                  tax_level,
                  taxon_col="taxon",
                  rankID_col="rankID",
                  taxlevel_col="taxlevel"):
    """
    Populate input node with daughter taxa nodes.

    Parameters
    -------
    df: pandas.DataFrame
        pandas.DataFrame read from mothur's tax.summary file.
    node: lxml.etree._Element
        Input node which will be populated with data selected with
        mothulity_draw.get_daughter_df.
    tax_level: int
        Taxon taxonomical level value of which daughter taxa will populate the input node.
    taxon_col: str
        Taxon column name in node's daughter pandas.DataFrame.
    rankID_col: str
        rank ID column name in node's daughter pandas.DataFrame.
    taxlevel_col: str
        Taxonomical level column name in node's daughter pandas.DataFrame.
    """
    node_tax_name = node.attrib["name"]
    node_rank = node.attrib["rankID"]
    children = get_daughter_df(df,
                               node_tax_name,
                               node_rank,
                               tax_level)
    if children is not None:
        for i in children.itertuples():
            et.SubElement(node,
                          "node",
                          name=str(getattr(i, taxon_col)),
                          rankID=str(getattr(i, rankID_col)),
                          taxlevel=str(getattr(i, taxlevel_col)))


def populate_tree(df,
                  nodes_root,
                  tax_levels):
    """
    Populate whole xml structure with daughter nodes using
    mothulity_draw.populate_node.

    Parameters
    -------
    df: pandas.DataFrame
        pandas.DataFrame read from mothur's tax.summary file.
    nodes_root: lxml.etree._Element
        Node from which populating will start.
    tax_levels: list
        Taxon taxonomical level values list.
    """
    check_list = []
    for tax_level in tax_levels:
        for i in nodes_root.iter():
            if i not in check_list:
                populate_node(df, i, tax_level)
            check_list.append(i)


def populate_count(df,
                   nodes_root,
                   groups,
                   taxon_col="taxon",
                   rankID_col="rankID",
                   taxlevel_col="taxlevel",
                   taxon_attrib="name",
                   rankID_attrib="rankID",
                   taxlevel_attrib="taxlevel"):
    """
    Populate each taxonomical node with count values.

    Parameters
    -------
    df: pandas.DataFrame
        pandas.DataFrame read from mothur's tax.summary file.
    nodes_root: lxml.etree._Element
        Node from which populating will start.
    taxon_col: str
        Taxon column name in corresponding pandas.DataFrame.
    rankID_col: str
        rank ID column name in corresponding pandas.DataFrame.
    taxlevel_col: str
        Taxonomical level column name in corresponding pandas.DataFrame.
    taxon_attrib: str
        Taxon attribute name in node.
    rankID: str
        rankID attribute name in node.
    taxlevel_attrib: str
        taxlevel attribute name in node.
    """
    for i in nodes_root.iter():
        if len(i.attrib) >= 3:
            sel_df = df[(df[taxon_col] == i.attrib[taxon_attrib]) &
                        (df[taxlevel_col] == int(i.attrib[taxlevel_attrib])) &
                        (df[rankID_col] == i.attrib[rankID_attrib])]
            values = sel_df[groups].values.tolist()[0]
            count_elem = et.SubElement(i, "count")
            for ii in values:
                et.SubElement(count_elem, "val").text = str(ii)


def constr_krona_xml(input_file_name,
                     output_file_name,
                     sep="\t",
                     root_tag="krona",
                     attributes_tag="attributes",
                     attribute_tag="attribute",
                     attribute_text="count",
                     datasets_tag="datasets",
                     dataset_tag="dataset",
                     root_node_tag="node",
                     attributes_dict={"magnitude": "count"},
                     attribute_dict={"display": "Count"},
                     root_node_dict={"name": "Root",
                                     "rankID": "0",
                                     "taxlevel": "0"}):
    """
    Convert mothur's tax.summary file to ktImportXML compatible xml file.

    Parameters
    -------
    input_file_name: str
        Input file name.
    output_file_name: str
        Output file name.
    sep: str, default <\t>
        Separator in input file.
    """
    df = pd.read_csv(input_file_name, sep=sep)
    groups_list = list(df.columns[5:])
    tax_lev_list = list(df.taxlevel.drop_duplicates())
    root = et.Element(root_tag)
    attributes = et.SubElement(root, attributes_tag, attributes_dict)
    attribute = et.SubElement(attributes, attribute_tag, attribute_dict)
    attribute.text = attribute_text
    datasets = et.SubElement(root, datasets_tag)
    for i in groups_list:
        et.SubElement(datasets, dataset_tag).text = i
    root_node = et.SubElement(root, root_node_tag, root_node_dict)
    populate_tree(df,
                  root_node,
                  tax_lev_list)
    populate_count(df,
                   root_node,
                   groups_list)
    elements_tree = et.ElementTree(root)
    elements_tree.write(output_file_name,
                        pretty_print=True,
                        xml_declaration=True,
                        encoding="utf-8")


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
    parser.add_argument("-o",
                        "--output",
                        dest="output_file_name",
                        default=None,
                        help="output file name")
    parser.add_argument("--rarefaction",
                        action="store_true",
                        dest="rarefaction",
                        default=False,
                        help="Draw rarefaction curves plot.")
    parser.add_argument("--phylip",
                        action="store_true",
                        dest="phylip",
                        default=False,
                        help="Draw heatmap")
    parser.add_argument("--tree",
                        action="store_true",
                        dest="tree",
                        default=False,
                        help="Draw dendrogram.")
    parser.add_argument("--axes",
                        action="store_true",
                        dest="axes",
                        default=False,
                        help="Draw scatter plots.")
    parser.add_argument("--summary-table",
                        action="store_true",
                        dest="summary_table",
                        help="Convert summary table into fancy DataTable.")
    parser.add_argument("--krona-xml",
                        action="store_true",
                        dest="krona_xml",
                        default=False,
                        help="Convert mothur's tax.summary file to\
                        krona-compatible xml.")
    parser.add_argument("--render-html",
                        action="store_true",
                        dest="render_html",
                        default=False,
                        help="Pass args into fancy html.")
    args = parser.parse_args()

    config_path_abs = get_dir_path("mothulity.config")
    config = ConfigParser.SafeConfigParser()
    config.read(config_path_abs)
    datatables_css = config.get("css", "datatables")
    datatables_js = get_dir_path(config.get("js", "datatables"))

    if args.rarefaction is True:
        draw_rarefaction(args.input_file_name, args.output_file_name)
    if args.phylip is True:
        draw_heatmap(args.input_file_name, args.output_file_name)
    if args.tree is True:
        draw_tree(args.input_file_name, args.output_file_name)
    if args.axes is True:
        draw_scatter(args.input_file_name, args.output_file_name)
    if args.summary_table is True:
        summary2html(args.input_file_name,
                     args.output_file_name,
                     datatables_css,
                     datatables_js)
    if args.krona_xml is True:
        constr_krona_xml(args.input_file_name, args.output_file_name)


if __name__ == '__main__':
    main()
