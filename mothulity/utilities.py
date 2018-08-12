#! /usr/bin/env python


from __future__ import print_function
import six
import sys
import os
from glob import glob
from six.moves import configparser
import jinja2 as jj2
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests as rq
from tqdm import tqdm
from Bio import Phylo as ph
import matplotlib
matplotlib.use('Agg')
import pylab
import matplotlib.pyplot as plt
import matplotlib.style as style
import mpld3
import numpy as np
from pandas import read_csv
from seaborn import heatmap
from seaborn import pairplot
from seaborn import lmplot
from lxml import etree as et


def get_dir_path(file_name=""):
    """
    Find out what is the script system path and return its location. Optionally
    put desired file name at the end of the path. Facilitates access to files
    stored in the same directory as executed script. Requires the executed
    script being added to the system path

    Parameters
    --------
    file_name: str, default <"">
        File name to put at the end of the path. Use empty string if want just
        the directory.

    Returns
    --------
    str
        System path of the executable.

    Examples
    -------
    >>> get_dir_path() # doctest: +SKIP
    '/home/user/program/bin/'
    >>> get_dir_path("foo") # doctest: +SKIP
    '/home/user/program/bin/foo'
    """
    # prog_path = sys.argv[0].replace(sys.argv[0].split("/")[-1],
    #                                 file_name)
    prog_path = "/".join(sys.argv[0].split("/")[:-1] + [file_name])
    return os.path.abspath(prog_path)


def path2name(path,
              slash="/",
              hid_char=".",
              extension=False):
    """
    Returns just filename with or without extension from the full path.

    Parameters
    -------
    path: str
        Input path.
    slash: str
        Slash to use. Backslash does NOT work properly yet. Default: </>.
    hid_char: str
        Character indicating that file is hidden. Default: <.>
    extension: bool
        Return filename with extension if <True>. Remove extension\
        otherwise. Default: <False>.

    Returns
    -------
    str
        Filename from the path.

    Examples
    -------
    >>> path2name("/home/user/foo.bar")
    'foo'
    >>> path2name("/home/user/.foo.bar")
    'foo'
    >>> path2name("/home/user/foo.bar", extension=True)
    'foo.bar'
    >>> path2name("/home/user/.foo.bar", extension=True)
    'foo.bar'
    """
    if extension is True:
        return str(path.split(slash)[-1].strip(hid_char))
    else:
        return str(path.split(slash)[-1].strip(hid_char).split(".")[0])


def set_config(filename,
               section,
               options,
               values,
               clean=False):
    if os.path.exists(filename):
        config = configparser.ConfigParser()
        config.read(os.path.abspath(filename))
        if clean and section in config.sections():
            config.remove_section(section)
        if section not in config.sections():
            config.add_section(section)
        for o, v in zip(options, values):
            config.set(section, o, v)
        with open(filename, "w") as fout:
            config.write(fout)
    else:
        return None


def load_template_file(template_file,
                       searchpath="/"):
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

    Examples
    -------
    >>> import jinja2
    >>> lt = load_template_file("./tests/test.jj2", searchpath=".")
    >>> isinstance(lt, jinja2.environment.Template)
    True
    """
    template_Loader = jj2.FileSystemLoader(searchpath=searchpath)
    template_Env = jj2.Environment(loader=template_Loader)
    template = template_Env.get_template(template_file)
    return template


def render_template(template_loaded,
                    template_vars):
    """
    Render jinja2.Template to unicode.

    Parameters
    -------
    loaded_template: jinj2.Template
        Template to render.
    template_vars: dict
        Variables to be rendered with the template.

    Returns
    -------
    unicode
        Template content with passed variables.

    Examples
    -------
    >>> lt = load_template_file("./tests/test.jj2",\
    searchpath=".")
    >>> vars = {"word1": "ipsum", "word2": "adipisicing", "word3": "tempor"}
    >>> rt = render_template(lt, vars)
    >>> str(rt)
    'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt.'
    """
    template_rendered = template_loaded.render(template_vars)
    return template_rendered


def save_template(out_file_name,
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
    with open(out_file_name, "wb") as fout:
        fout.write(template_rendered.encode("utf-8"))


def read_info_shared(input_file_name,
                     min_fold=5,
                     label_col="label",
                     group_col="Group",
                     otu_col="Otu",
                     num_col="numOtus",
                     sep="\t",
                     format_junk_grps=True):
    """
    Extracts information from mothur's shared file.

    Parameters
    -------
    input_file_name: str
        Input file name.
    min_fold: int
        Fraction of mean group size below which groups will be removed before
        analysis.
    label_col: str
        Label column name in shared file.
    group_col: str
        Group column name in shared file.
    otu_col: str
        OTU column name prefix in shared file.
    num_col: str
        Number of OTUs column name in shared file.
    sep: str, default <\t>
        Delimiter to use for reading-in shared file.
    format_junk_grps: bool, default <True>
        Join names of groups to remove by <-> before passing to mothur.

    Returns
    -------
    dict
        Information about label, number of samples and groups to remove.

    Examples
    -------
    >>> shared_info = read_info_shared(input_file_name="./tests/test.shared")
    >>> shared_info["samples_number"]
    9
    >>> float(shared_info["label"])
    0.03
    >>> shared_info["junk_grps"]
    'F3D141-F3D143-F3D144'
    """
    dtypes = {label_col: "str"}
    shared_df = pd.read_csv(input_file_name, sep=sep, dtype=dtypes)
    otus_cols = [i for i in shared_df.columns if otu_col in i and i != num_col]
    grps_sizes = shared_df[[group_col] + otus_cols].sum(axis=1)
    label = shared_df[label_col][0]
    grps_num = len(shared_df[group_col])
    sizes_df = pd.DataFrame({"GROUPS": shared_df[group_col],
                             "GROUP_SIZES": grps_sizes})
    threshold = sizes_df.GROUP_SIZES.mean() / min_fold
    size_bool = (sizes_df.GROUP_SIZES < threshold)
    junk_grps = list(sizes_df[size_bool].GROUPS)
    if format_junk_grps is True:
        junk_grps = "-".join(junk_grps)
    out_dict = {"label": label,
                "samples_number": grps_num,
                "junk_grps": junk_grps}
    return out_dict


def parse_html(input_file_name,
               html_type,
               parser="html.parser",
               newline="\n"):
    """
    Extract particular tags from html so that they can be placed in
    another html without iframe.

    Parameters
    -------
    input_file_name: str
        Input file name.

    """
    with open(input_file_name) as fin:
        html = fin.read()
    soup = bs(html, parser)
    if html_type == "krona":
        head = [str(i) for i in soup.head if i != newline]
        body = [str(i) for i in soup.body if i != newline]
        return {"head": {"link": head[1],
                         "script_not_found": head[2],
                         "script_functional": head[3]},
                "body": {"img_hidden": body[0],
                         "img_loading": body[1],
                         "img_logo": body[2],
                         "noscript": body[3],
                         "div_krona": body[4]}}
    elif html_type == "summary":
        tags = [str(i) for i in list(soup.children) if i != "\n"]
        return {"link": tags[0],
                "table": tags[1],
                "googleapis_script": tags[3],
                "datatables_script": tags[4],
                "script": tags[5]}
    elif html_type == "rarefaction" or html_type == "nmds":
        return {"div": str(soup.div),
                "script": str(soup.script)}


def names_sanitizer(files_directory,
                    unwanted_sign):
    """
    Remove desired sign from file names from all files in given directory.

    Parameters
    -------
    files_directory: str
        Input directory.
    unwanted_sign: str,
        Sign to be removed from file names.

    Examples
    -------
    >>> import os
    >>> open("./tests/test-test-test.test", "wb").close()
    >>> names_sanitizer("./tests", "-")
    >>> "testtesttest.test" in os.listdir("./tests/")
    True
    """
    for i in os.listdir(files_directory):
        if unwanted_sign in i:
            os.rename("{0}/{1}".format(files_directory,
                                       i),
                      "{0}/{1}".format(files_directory,
                                       i.replace(unwanted_sign, "")))


def left_n_right_generator(files_directory,
                           split_sign="_",
                           files_extension="fastq",
                           left_reads_sign="R1",
                           right_reads_sign="R2"):
    """
    Returns dict containing two lists of file names. Names are divided into
    sections by split sign. Then, names are recognized as left or right by
    given set of characters.

    Parameters
    -------
    files_directory: str
        Input directory.
    split_sign: str, default <_>
        Character by which file names are split into sections.
    files_extension: str, default <fastq>
        Only file names with this extensions are taken as input.
    left_reads_sign: str, default <R1>
        Set of characters by which file names are recognized as left.
    right_reads_sign: str, default <R2>
        Set of characters by which file names are recognized as right.

    Returns
    -------
    dict of lists
        Dict with <left> and <right> keywords and two lists of str as values.

    Examples
    -------
    >>> filenames = left_n_right_generator("./tests")
    >>> filenames["left"][0]["name"]
    'test1'
    >>> filenames["left"][0]["left_reads"]
    './tests/test1_S001_R1.fastq'
    >>> filenames["right"][0]["right_reads"]
    './tests/test1_S001_R2.fastq'
    >>> filenames["left"][1]["name"]
    'test2'
    >>> filenames["left"][1]["left_reads"]
    './tests/test2_S001_R1.fastq'
    >>> filenames["right"][1]["right_reads"]
    './tests/test2_S001_R2.fastq'
    """
    left_name_reads_list = []
    right_name_reads_list = []
    files_list = os.listdir(files_directory)
    files_list = [i for i in files_list if files_extension == i.split(".")[-1]]
    sample_names_list = [i.split(split_sign)[0] for i in files_list]
    sample_names_list = sorted(list(set(sample_names_list)))
    for i in sample_names_list:
        for ii in files_list:
            if i == ii.split(split_sign)[0] and left_reads_sign in ii:
                left_name_reads_list.append({"name": i, "left_reads": "{0}/{1}".format(files_directory, ii)})
            elif i == ii.split(split_sign)[0] and right_reads_sign in ii:
                right_name_reads_list.append({"name": i, "right_reads": "{0}/{1}".format(files_directory, ii)})
            else:
                pass
    name_reads = {"left": left_name_reads_list,
                  "right": right_name_reads_list}
    return name_reads


def get_db(url,
           save_path,
           chunk=8192):
    """
    Download from url to file. Handles different chunk sizes saving RAM. Shows
    progress with tqdm progress bar.

    Parameters
    -------
    url: str
        URL to download from.
    save_path: str
        Local URL to save to.
    chunk: int, default 8192
        Size of chunk the stream is divided to. Smaller it is less memory it
        uses.

    Examples
    -------
    >>> import os
    >>> get_db("http://google.com", "./tests/google.html")
    200
    >>> os.path.getsize("./tests/google.html") > 0
    True
    """
    res = rq.get(url, stream=True)
    total_len = int(res.headers.get("content-length"))
    if res.status_code == 200:
        with open(save_path, "wb") as fout:
            for i in tqdm(res.iter_content(chunk_size=chunk),
                          total=total_len / chunk):
                fout.write(i)
    return res.status_code


def download(download_directory,
             filename,
             url,
             command,
             input_arg,
             output_arg):
    """
    Download and unpack specified database into specified directory.

    Parameters
    -------
    db_type: str
        Database name which determines the download URL and archive type.
    download_directory: str
        Path where the database files would be downloaded.
    """
    download_path = "{}/{}".format(download_directory, filename)
    print("Download path: {}".format(download_path))
    print("Connecting...")
    try:
        res = get_db(url, download_path)
        if res == 200:
            print("Downloading done!")
            print("Unpacking...")
            os.system("{} {} {} {} {}".format(command,
                                              input_arg,
                                              download_path,
                                              output_arg,
                                              download_directory))
            os.system("rm {}".format(download_path))
            print("Unpacking done!")
        else:
            print("Failed to establish connection. Response code {}".format(res))
    except Exception as e:
        print("Failed to establish connection.")


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
    with open(output_file_name, "wb") as fout:
        fout.write(mpld3.fig_to_html(fig).encode('utf-8'))


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
    df.index.name = None
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
                 axis1_col="axis1",
                 axis2_col="axis2",
                 group_col="group",
                 title_text="Scatter plot",
                 title_size=20,
                 point_size=100,
                 point_alpha=0.3,
                 grid_color="white",
                 grid_style="solid",
                 backgroud_color="#EEEEEE",
                 sep="\t"):
    """
    Draw scatter plot from mothur's axes file and save figure to file.

    Parameters
    -------
    input_file_name: str
        Input file name.
    output_file_name: str
        Output file name.
    axis1_col: str, default <axis1>
        Axis 1 column name in axis file.
    axis2_col: str, default <axis2>
        Axis 2 column name in axis file.
    group_col: str, default <group>
        Group column name in axis file.
    title_text: str, default <Scatter plot>
        Text displayed as plot title.
    title_size: int, default <20>
        Plot title size.
    point_size: int, default <100>
        Point size.
    point_alpha: float, default <0.3>
        Point transparency.
    grid_color: str, default <white>
        Color of the plot grid.
    grid_style: str, default <solid>
        Style of the plot grid.
    backgroud_color: str, default <#EEEEEE>
        Color of the plot backgroud.
    sep: str, default <\t>
        Delimiter to use for reading-in axes file.
    """
    df = read_csv(input_file_name,
                  sep=sep)
    fig, ax = plt.subplots()
    scatter = ax.scatter(np.array(df[axis1_col]),
                         np.array(df[axis2_col]),
                         c=np.random.random(size=len(df)),
                         s=100,
                         alpha=0.3,
                         cmap=plt.cm.jet)
    ax.grid(color=grid_color, linestyle=grid_style)
    ax.set_title(title_text, size=title_size)
    labels = list(df[group_col])
    tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=labels)
    mpld3.plugins.connect(fig, tooltip)
    mpld3.save_html(fig, output_file_name)


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
                                  js_str).encode("utf-8")
    with open(output_file_name, "wb") as fout:
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
        daughter_df = df[df.rankID.str.contains('^{}\.\d+$'.format(mother_rank))]
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
