import csv
from git import Git
from pydriller import Repository
from datetime import datetime

header = ['Test-filename', 'File-path', 'Modification-type', 'Commit-date', 'Author-Name']

with open('testreport_mining.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for commit in Repository('https://github.com/open-mpi/ompi',filepath='test').traverse_commits():
        for modifiedfile in commit.modified_files:
            oldpath = modifiedfile.old_path
            newpath = modifiedfile.new_path
            if (oldpath is None):
                if (newpath.startswith('test') and (newpath.endswith('.c'))):
                    list=[]
                    list.append(modifiedfile.filename)
                    list.append(modifiedfile.new_path)
                    list.append("Added")
                    list.append(commit.committer_date)
                    list.append(commit.author.name)
                    writer.writerow(list)
            elif (newpath is None):
                if (oldpath.startswith('test') and (oldpath.endswith('.c'))):
                    list=[]
                    list.append(modifiedfile.filename)
                    list.append(modifiedfile.old_path)
                    list.append("Deleted")
                    list.append(commit.committer_date)
                    list.append(commit.author.name)
                    writer.writerow(list)
            else:
                if (newpath.startswith('test') and (newpath.endswith('.c'))):
                    list=[]
                    list.append(modifiedfile.filename)
                    list.append(modifiedfile.new_path)
                    list.append("Modified")
                    list.append(commit.committer_date)
                    list.append(commit.author.name)
                    writer.writerow(list)


