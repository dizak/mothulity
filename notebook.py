import os
import pandas as pd

output_file_name = "zury_V3_V4"
split_sign = "_"
left_reads_sign = "R1"
right_reads_sign = "R2"
files_directory = "/home/darek/Pulpit/zury_V3_V4/"
files_extension = "fastq"
files_list = os.listdir(files_directory)
sample_names_list = [i.split(split_sign)[0] for i in files_list if files_extension in i]
sample_names_list = list(set(sample_names_list))
left_name_reads_list = []
right_name_reads_list = []
for i in sample_names_list:
    for ii in files_list:
        if i in ii and left_reads_sign in ii:
            left_name_reads_list.append({"name": i, "left_reads": ii})
        elif i in ii and right_reads_sign in ii:
            right_name_reads_list.append({"name": i, "right_reads": ii})
        else:
            pass




files_dataframe = pd.merge(left=pd.DataFrame(left_name_reads_list),
                           right=pd.DataFrame(right_name_reads_list),
                           on="name")
files_dataframe[["name", "left_reads", "right_reads"]].to_csv("{}.files".format(output_file_name),
                                                              sep="\t",
                                                             index=False)
