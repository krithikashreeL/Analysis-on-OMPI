import os
import collections
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.dates


## QUESTION I
## LANGUAGE DISTRIBUTION
extensions = collections.defaultdict(int)
root = "D:/PAT/openmpi-4.1.2"
for path, dirs, files in os.walk(root):
   for filename in files:
       extensions[os.path.splitext(filename)[1].lower()] += 1
count_files = []


language = ['.c','.cc','.f','.f90','.java','.py','.trs','.am','.in']
with open('extn_count_lang.csv', 'w') as f:
    for key in extensions.keys():
       # if int(extensions[key]) > 10 :
       if key in language:
            f.write("%s,%s\n" % (key, extensions[key]))

lang = []
count = []
with open('extn_count_lang.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')

    for row in plots:
        lang.append(row[0])
        count.append(int(row[1]))

plt.bar(lang, count, color='steelblue', width=0.72, label="Count")
#plt.fill_between(x, 0, y, alpha=.3)

plt.xlabel('Used Programming Languages')
plt.ylabel('Count')
plt.title('Programming languages used in this repository')
plt.show()

## LAYERS OF OMPI

cwd = os.getcwd()
cwd = "E:\PAT\openmpi-4.1.3"
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
    ompi_count = 0
    opal_count = 0
    orte_count = 0
    if (r'ompi' in path):
        #print(1)
        for filename in files:
            ompi_count = ompi_count + 1
    if (r'ompi\opal' in path):
        for filename in files:
            opal_count += 1
    if (r'orte' in path):
        for filename in files:
            orte_count += 1

orte_count = 2297
opal_count = 5064
ompi_count = 15472
Count = [2297,5064,15472]
Layer = ['ORTE','OPAL','OMPI']

plt.bar(Layer,Count, color='steelblue', width=0.72, label="Count")
plt.xlabel('Layers of OMPI')
plt.ylabel('Count')
plt.title('Development across different layers of OMPI Architecture')
plt.show()
plt.show()

## LINE COVERAGE STATS
coverage= []
file = []
fun = []
path_to_csv= "E:/PAT/openmpi-4.1.3/coveragr_result.csv"
with open(path_to_csv, 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        val = row[3].split('%')
        dt_obj = val[0]
        val = row[6].split('%')
        ft_obj = val[0]
        if dt_obj != "line_percent":
            #print(type(float(dt_obj)))
            if float(dt_obj) > 0.0:
                coverage.append(float(dt_obj))
                file.append(row[0])



    plt.bar(file,coverage, color='steelblue', width=0.72, label="Count")
    plt.xticks(rotation=90,fontsize=5)
    plt.xlabel('Files')
    plt.ylabel('Coverage')
    plt.title('Line coverage statistics with average '+str(np.mean(coverage))+'.', fontsize=20)
    plt.show()

### QUESTION 4

## COMMIT TYPE PLOT
modification_type = []
file_name = []

with open('project-report.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
            modification_type.append(row[2])
            file_name.append(row[0])


d = {'modification_type':modification_type,'file_name':file_name}
df = pd.DataFrame(d)
df = df.iloc[1: , :]
df = df.groupby(['modification_type']).size()
# df = pd.DataFrame(occur)
print(df)
colors = ["#EC6B56","#FFC154","#47B39C"]
explode = (0.125, 0, 0)
df.plot.pie(explode=explode, colors=colors,autopct='%1.1f%%', shadow=True, startangle=140)
plt.title("Ratio of addition to deletion and modification")
plt.ylabel('')
plt.show()

## ADDITION STATS

root = "D:/PAT/openmpi-4.1.2"
lang = []
count = []

with open('project-report.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        if row[2] == "Added":
            lang.append(row[4])
            val = row[3].split(' ')
            dt_obj = val[0]
            count.append(dt_obj)



plt.plot(count, lang, color='steelblue', linestyle='dashed',
         marker='o', label="Test file Addition statistics for master")

plt.xticks(rotation=90)
plt.xlabel('Dates')
plt.ylabel('Tester')
plt.title('Test file Addition statistics for master', fontsize=20)
#plt.grid()
plt.show()

## MODIFICATION STATS

lang = []
count = []

with open('project-report.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        if row[2] == "Modified":
            lang.append(row[0])
            val = row[3].split(' ')
            dt_obj = val[0]
            count.append(dt_obj)

converted_dates = matplotlib.dates.datestr2num(count)




d = {'Author':lang,'Time':converted_dates}
df = pd.DataFrame(d)

# count occurrences a particular column
occur = df.groupby(['Author']).size()
df = pd.DataFrame(occur)
df.plot(kind='bar')

plt.xticks(rotation=90,fontsize=5)
plt.xlabel('Filename')
plt.ylabel('Frequency')
plt.title('Test file Modification statistics for master', fontsize=20)
# plt.grid()
plt.show()

## CONTRIBUTERS STATS

ppl_involved = []

with open('project-report.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
            ppl_involved.append(row[4])
tester = (len(set(ppl_involved)))
total = 237
table = [tester,total]
df = pd.DataFrame(table)
colors = ["#EC6B56","#F7B7A3"]
lable = ["Testers","Total Contributers"]
explode = (0.12, 0)
df.plot.pie(labels=lable,explode=explode, colors=colors,autopct='%1.1f%%', shadow=True, startangle=140,subplots=True,legend=None)
plt.title("Ratio of Tester to total contributers")
plt.ylabel('')
plt.show()

## ISSUES
issue = []
opens = []
close = []
lable = ['Auto closed','bug','code cleanup','enhancement','performance','memory leak','invalid']

with open('labels-issues.csv', 'r',encoding="utf8") as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        if row[0] in lable:
            issue.append(row[0])
            opens.append(row[1])
            close.append(row[2])

    x = np.arange(len(issue))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, opens, width, label='Open Issues')
    rects2 = ax.bar(x + width / 2, close, width, label='Closed Issues')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Issues')
    ax.set_title('Issue Statistics')
    ax.set_xticks(x, issue)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()

    plt.show()


##  Question-2-Assert statements count in each test files
test_assert_files = []
test_assert_count = []
header = 1
total_assert_files = 0
total_test_files = 0
with open(r'C:\Users\gspav\OneDrive\Desktop\pat_project\2_test_assertcount.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        if (header == 1):
            header = 0
        else:
            print(row)
            test_assert_files.append(row[0])
            test_assert_count.append(int(row[1]))
            if (int(row[1]) > 0):
                total_assert_files = total_assert_files + 1
            total_test_files = total_test_files + 1

plt.xlabel('Test Filename')
plt.ylabel('Testfile_Assert_Count')
plt.title('Assert count for each test file', fontsize=15)
plt.plot(test_assert_files, test_assert_count, color='steelblue', linestyle='dashed',
         marker='.', label="Test file Addition statistics for master")

plt.show()

##  Question-2-Total test files and files with assert statements count greater than zero
a = []
t = []
a.append(total_assert_files)
t.append(total_test_files)
test_assert = dict(zip(a, t))
d_f = pd.DataFrame(list(test_assert.items()), columns=['Assert_count>0', 'Testfile_count'])
d_f.plot(kind='bar', stacked=True, width=0.1)
plt.title("Test files and Assert statements count")
plt.ylabel("Count")
plt.xticks([])
plt.show()

##  Question-3-File wise assert and debug statements count
f = []
a = []
d = []
header = 1
with open(r'C:\Users\gspav\OneDrive\Desktop\pat_project\filename_assert_debug.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for rows in plots:
        if (header == 1):
            header = 0
        else:
            print(rows)
            f.append(rows[0])
            a.append(int(rows[1]))
            d.append(int(rows[2]))

df = pd.DataFrame(f, columns=['FileName'])
df.insert(loc=1, column='Assert_Count', value=a, allow_duplicates=True)
df.insert(loc=2, column='Debug_Count', value=d, allow_duplicates=True)

print(df)
index = np.arange(len(a))
bar_width = 0.35

fig, ax = plt.subplots()

a_count = ax.bar(index, df["Assert_Count"], bar_width,
                 label="Assert")

d_count = ax.bar(index + bar_width, df["Debug_Count"],
                 bar_width, label="Debug")
ax.set_xlabel('Filenames')
ax.set_ylabel('Count')
ax.set_title('Assert and Debug count for production files')
ax.set_xticklabels([])
ax.legend()

plt.show()

## Question-3-Assert count for each Folder considering production files


l1 = []
l2 = []
header = 1
with open(r'C:\Users\gspav\OneDrive\Desktop\pat_project\folder_assert.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for rows in plots:
        if (header == 1):
            header = 0
        else:
            #print(rows)
            l1.append(rows[0])
            l2.append(int(rows[1]))

dict_folder = dict(zip(l1, l2))
df_folder = pd.DataFrame(list(dict_folder.items()), columns=['Folder', 'Count_assert_statements'])
plt.xticks(rotation=90)
plt.xlabel('Folder')
plt.ylabel('Count_assert_statements')
plt.title('Assert count for each Folder considering production files', fontsize=15)
plt.plot(l1, l2, color='blue', linestyle='dashed',
         marker='.', label="Test file Addition statistics for master")

plt.show()

## Question-3-Debug count for each Folder considering production files


l1 = []
l2 = []
header = 1
with open(r'C:\Users\gspav\OneDrive\Desktop\pat_project\folder_debug.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for rows in plots:
        if (header == 1):
            header = 0
        else:
            #print(rows)
            l1.append(rows[0])
            l2.append(int(rows[1]))

dict_folder = dict(zip(l1, l2))
df_folder = pd.DataFrame(list(dict_folder.items()), columns=['Folder', 'Count_debug_statements'])
plt.xticks(rotation=90)
plt.xlabel('Folder')
plt.ylabel('Count_debug_statements')
plt.title('Debug count for each Folder considering production files', fontsize=15)
plt.plot(l1, l2, color='blue', linestyle='dashed',
         marker='.', label="Test file Addition statistics for master")

plt.show()

