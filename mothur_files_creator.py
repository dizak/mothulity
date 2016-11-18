#! /usr/bin/env python

import os
import argparse
import pandas as pd


def names_sanitizer(unwanted_sign,
                    files_directory):
    for i in os.listdir(files_directory):
        if unwanted_sign in i:
            os.rename("{0}/{1}".format(files_directory,
                                       i),
                      "{0}/{1}".format(files_directory,
                                       i.replace(unwanted_sign, "")))


def left_n_right_generator(files_directory,
                           split_sign,
                           files_extension,
                           left_reads_sign,
                           right_reads_sign):
    left_name_reads_list = []
    right_name_reads_list = []
    files_list = os.listdir(files_directory)
    sample_names_list = [i.split(split_sign)[0] for i in files_list if files_extension in i]
    sample_names_list = list(set(sample_names_list))
    for i in sample_names_list:
        for ii in files_list:
            if i in ii and left_reads_sign in ii:
                left_name_reads_list.append({"name": i, "left_reads": ii})
            elif i in ii and right_reads_sign in ii:
                right_name_reads_list.append({"name": i, "right_reads": ii})
            else:
                pass
    name_reads = {"left": left_name_reads_list,
                  "right": right_name_reads_list}
    return name_reads


def main():
    parser = argparse.ArgumentParser(description = "creates mothur-suitable\
                                                    <.files> file just upon the\
                                                    input file names. removes\
                                                    <-> from file names",
                                     version = "tests")
    parser.add_argument(action = "store",
                        dest = "files_directory",
                        metavar = "path/to/files",
                        help = "input directory path.")
    parser.add_argument("--output",
                        action = "store",
                        dest = "output_file_name",
                        default = "mothur.files",
                        help = "output file name")
    parser.add_argument("--split-sign",
                        action = "store",
                        dest = "split_sign",
                        required = True,
                        help = "first group of characters before this sign is\
                                recognized as sample name.")
    parser.add_argument("--files-extension",
                        action = "store",
                        dest = "files_extension",
                        required = True)
    parser.add_argument("--left-reads-sign",
                        action = "store",
                        dest = "left_reads_sign",
                        required = True)
    parser.add_argument("--right-reads-sign",
                        action = "store",
                        dest = "right_reads_sign",
                        required = True)
    parser.add_argument("--original-names",
                        action = "store_true",
                        dest = "original_names",
                        default = False,
                        help = "use if you do not want to modify file names")
    args = parser.parse_args()

    if args.original_names == False:
        names_sanitizer("-",
                        args.files_directory)
    else:
        pass
    left_n_right = left_n_right_generator(args.files_directory,
                                          args.split_sign,
                                          args.files_extension,
                                          args.left_reads_sign,
                                          args.right_reads_sign)
    files_dataframe = pd.merge(left=pd.DataFrame(left_n_right["left"]),
                               right=pd.DataFrame(left_n_right["right"]),
                               on="name")
    files_dataframe[["name", "left_reads", "right_reads"]].to_csv(args.output_file_name,
                                                                  sep="\t",
                                                                  index = False,
                                                                  header = False)

if __name__ == "__main__":
    main()
