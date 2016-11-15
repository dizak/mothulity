#! /usr/bin/env python

import os
import argparse
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description = "mothur files creator",
                                     version = "tests")
    parser.add_argument("--input",
                        action = "store",
                        dest = "files_directory",
                        required = True,
                        help = "path to input directory.")
    parser.add_argument("--output",
                        action = "store",
                        dest = "output_file_name",
                        default = "mothur.files",
                        help = "path to output directory. Default:\
                                working directory")
    parser.add_argument("--split-sign",
                        action = "store",
                        dest = "split_sign",
                        required = True)
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
    args = parser.parse_args()

    files_list = os.listdir(args.files_directory)
    sample_names_list = [i.split(args.split_sign)[0] for i in files_list if args.files_extension in i]
    sample_names_list = list(set(sample_names_list))
    left_name_reads_list = []
    right_name_reads_list = []
    for i in sample_names_list:
        for ii in files_list:
            if i in ii and args.left_reads_sign in ii:
                left_name_reads_list.append({"name": i, "left_reads": ii})
            elif i in ii and args.right_reads_sign in ii:
                right_name_reads_list.append({"name": i, "right_reads": ii})
            else:
                pass
    files_dataframe = pd.merge(left=pd.DataFrame(left_name_reads_list),
                               right=pd.DataFrame(right_name_reads_list),
                               on="name")
    files_dataframe[["name", "left_reads", "right_reads"]].to_csv(args.output_file_name,
                                                                  sep="\t",
                                                                  index=False)

if __name__ == "__main__":
    main()
