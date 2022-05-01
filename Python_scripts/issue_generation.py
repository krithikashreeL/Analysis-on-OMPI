#the below import is from module PyGithub which can be installed with pip install PyGithub
from github import Github
import csv


token="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" #github user personal access token
g = Github(token)
repo = g.get_repo("open-mpi/ompi")

header = ['Label-name', 'open-issues-count', 'closed-issues-count']

with open('labels-issues.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    labels = repo.get_labels()
    for label in labels:
        opencount = 0
        closedcount = 0
        list=[]
        list.append(label.name)
        openissues = repo.get_issues(state='open',labels=[label.name])
        for issue in openissues:
            opencount = opencount + 1
        list.append(opencount)
        closedissues = repo.get_issues(state='closed',labels=[label.name])
        for issue in closedissues:
            closedcount = closedcount + 1
        list.append(closedcount)
        writer.writerow(list)

