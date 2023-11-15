__author__ = 'scottsfarley'
import csv
import requests

f = open("./data/expanded_extra_2.csv", 'r')
reader = csv.reader(f)
fout = open("./data/expanded_with_num_sites.csv", 'w')
writer = csv.writer(fout, lineterminator="\n")
i=0
for row in reader:
    endpoint = "http://api.neotomadb.org/v2.0/data/occurrences?taxonid=" + str(row[0])
    r = requests.get(endpoint)
    j = r.json()
    data = j['data']
    numSites = len(data)
    row.insert(3, numSites)
    writer.writerow(row)
    i += 1
    if i % 100 == 0:
        print(i)