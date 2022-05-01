import re
import os
import argparse
import csv
from collections import OrderedDict
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
def debug_assert_function(search_char, keyword):
    cwd = os.getcwd()

    cwd = cwd + "\ompi"
    total_assert_count = 0
    test_files_count = 0
    total_assert_files = 0
    path_count_dict = {}
    data = []
    prev_len = 0
    l_filepath = []
    l_count = []
    for path, subdirs, files in os.walk(cwd):
        prev_dir_count = 0
        path_status = 0
        if (r'ompi\test' not in path):
            for filename in files:
                count = 0
                try:
                    if (filename.endswith(".c") or filename.endswith(".h")):
                        path_of_file = path + "\\" + filename
                        file1 = open(path_of_file, 'r+')
                        read_line = file1.readlines()
                        for line in read_line:
                            if (re.search(search_char, line)):
                                count = count + 1
                        if (count > 0):
                            path_status = 1
                            prev_dir_count = count + prev_dir_count

                            total_assert_files = total_assert_files + 1
                            l_filepath.append(path + "--" + filename)
                            l_count.append(count)
                except UnicodeDecodeError:
                    print("File ", filename, "can not be decoded")

        curr_len = len(data)
        if (path_status == 1):

            path_count_dict[str(path)] = [prev_dir_count, prev_len, curr_len]
            total_assert_count = total_assert_count + prev_dir_count
        else:
            path_count_dict[str(path)] = [0, 0, 0]
            if (r'ompi\test' not in path):
                path_count_dict[str(path)] = [0, prev_len, curr_len]

        prev_len = curr_len

    temp_path_count_dict = path_count_dict
    path_count_list = sorted(list(path_count_dict.items()), key=lambda key: len(key[0]), reverse=True)
    res = {ele[0]: ele[1] for ele in path_count_list}
    path_count_dict = {path_count_list[i][0]: path_count_list[i][1] for i in range(0, len(path_count_list))}

    spec_str = '\\'
    for parent_rows in path_count_dict:
        string1 = str(parent_rows)
        for rows in path_count_dict:
            if (string1 in rows):
                string2 = str(rows)
                string2 = str(string2.replace(string1, ''))

                i_count = 0
                for i in string2:
                    if (i == spec_str):
                        i_count = i_count + 1

                if (i_count == 1):
                    path_count_dict.update({string1: [path_count_dict.get(string1)[0] + path_count_dict.get(rows)[0],
                                                      path_count_dict.get(string1)[1],
                                                      path_count_dict.get(string1)[2]]})

    final_path_count_dict = {k: v for k, v in path_count_dict.items() if (r'ompi\test' not in k)}
    temp_path_count_dict = {k: v for k, v in temp_path_count_dict.items() if (r'ompi\test' not in k)}

    for rows in temp_path_count_dict:
        temp_path_count_dict.update({rows: final_path_count_dict.get(rows)})

    tail_list = []
    l1 = []
    l2 = []
    for rows in temp_path_count_dict:
        index = rows.find('ompi')
        test_list = re.findall(r'[^\\]+\\[^\\]+|.+', rows[index:])
        if (len(test_list) == 1):
            l1.append(test_list[0])
            l2.append(temp_path_count_dict.get(rows)[0])
    dict_folder = dict(zip(l1, l2))
    df_folder = pd.DataFrame(list(dict_folder.items()), columns=['Folder', 'Count_' + keyword + '_statements'])
    plt.xticks(rotation=90)
    plt.xlabel('Folder')
    plt.ylabel('Count_' + keyword + '_statements')
    plt.title(keyword + ' count for each Folder considering production files', fontsize=15)
    plt.plot(l1, l2, color='blue', linestyle='dashed',
             marker='.', label="Test file Addition statistics for master")

    plt.show()

    file_path = dict(zip(l_filepath, l_count))
    df_file_location = pd.DataFrame(list(file_path.items()), columns=['File_Location', keyword + '_Count'])

    df_file_location.to_csv(r'C:\Users\gspav\OneDrive\Desktop\filelocation_' + keyword + '.csv', index=False, header=True)

    return file_path

assert_dict = debug_assert_function(r"^\s*.(assert\(.*\))", "assert")

debug_dict = debug_assert_function(r"_debug", "debug")

max_len = max(len(assert_dict), len(debug_dict))
if (max_len == len(assert_dict)):
    temp_dict = assert_dict
else:
    temp_dict = debug_dict

assert_debug_dict = {}
for rows in assert_dict:
    assert_debug_dict[rows] = [assert_dict.get(rows), 0]
    if (debug_dict.get(rows)):
        assert_debug_dict.update({rows: [assert_debug_dict.get(rows)[0], debug_dict.get(rows)]})

for rows in debug_dict:
    if (assert_debug_dict.get(rows)):
        continue
    else:
        assert_debug_dict[rows] = [0, debug_dict.get(rows)]

assert_debug_dict1 = {k: v[0] for k, v in assert_debug_dict.items()}
assert_debug_dict2 = {k: v[1] for k, v in assert_debug_dict.items()}

f=[]
l=[]
value_list = list(assert_debug_dict.keys())
my_array = [phrase.split("--") for phrase in value_list]
for i in my_array:
    f.append(i[1])
a=[]
d=[]
l=assert_debug_dict.values()
for i in l:
    a.append(i[0])
    d.append(i[1])
df = pd.DataFrame(f, columns=['FileName'])
df.insert(loc=1, column='Assert_Count', value=a, allow_duplicates=True)
df.insert(loc=2, column='Debug_Count', value=d, allow_duplicates=True)

df.to_csv(r'C:\Users\gspav\OneDrive\Desktop\filename_assert_debug.csv', index=False, header=True)
index = np.arange(len(a))
bar_width = 0.35

fig, ax = plt.subplots()

a_count = ax.bar(index, df["Assert_Count"], bar_width,
                label="Assert")

d_count = ax.bar(index+bar_width, df["Debug_Count"],
                 bar_width, label="Debug")
ax.set_xlabel('Filenames')
ax.set_ylabel('Count')
ax.set_title('Assert and Debug count for production files')
#ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels([])
ax.axes.xaxis.set_ticklabels([])
ax.legend()

plt.show()