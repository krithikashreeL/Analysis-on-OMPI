import re
import os
#import git
import argparse
import csv
import pandas as pd
import matplotlib.pyplot as plt

from collections import OrderedDict

cwd = os.getcwd()
cwd = cwd + "\ompi"
print("Current working directory:", cwd)
total_assert_count = 0
test_files_count = 0
total_assert_files = 0
total_test_files = 0
path_count_dict = {}
data = []
prev_len = 0
filenames=[]
testfiles=[]
assert_count=[]
for path, subdirs, files in os.walk(cwd):
    prev_dir_count = 0
    path_status = 0
    if (r'ompi\test' in path):
        for filename in files:
            count = 0

            try:
                # print("filename: ",filename)
                if (filename.endswith(".c") or filename.endswith(".h")):
                    #print(filename)
                    path_of_file = path + "\\" + filename
                    file1 = open(path_of_file, 'r+')
                    read_line = file1.readlines()
                    for line in read_line:
                        if (re.search(r"^\s*.(assert\(.*\))", line)):
                            count = count + 1
                    if (count >0):
                        path_status = 1
                        prev_dir_count = count + prev_dir_count

                        total_assert_files = total_assert_files + 1

                        # path_count_dict[str(path)]=prev_dir_count
                    # data=[]
                    filenames.append(filename)
                    assert_count.append(count)
                    #data.append([filename, count])
                    # data.append(count)
                    #print("filename: ", filename, "count: ", count)
                    # writer.writerow(data)
                    if(count>=0):
                        total_test_files = total_test_files + 1


            except UnicodeDecodeError:
                print("File ", filename, "can not be decoded")


print("Total number of files with assert count greater than zero are ",total_assert_files)
print("Total number of test files",total_test_files)
dict1_from_list = dict(zip(filenames, assert_count))
#print(dict1_from_list)
df = pd.DataFrame(list(dict1_from_list.items()),columns = ['Name of the File','Count of Assert statements'])

#print(df)
df.to_csv(r'C:\Users\gspav\OneDrive\Desktop\2_test_assertcount.csv', index=False, header=True)
#f_c=pd.DataFrame(total_assert_files,total_test_files)
#print(f_c)

plt.xticks(rotation=90)
plt.xlabel('Test Filename')
plt.ylabel('Testfile_Assert_Count')
plt.title('Assert count for each test file', fontsize=15)
plt.grid()
plt.plot(filenames, assert_count, color='black', linestyle='dashed',
         marker='.', label="Test file Addition statistics for master")

plt.show()
a=[]
t=[]
a.append(total_assert_files)
#print(a)
t.append(total_test_files)
#print(t)
test_assert = dict(zip(a, t))
d_f = pd.DataFrame(list(test_assert.items()),columns = ['Assert_count>0','Testfile_count'])
d_f.plot(kind='bar', stacked=True,width=0.1)
plt.title("Test files and Assert statements count")
plt.ylabel("Count")

plt.show()
