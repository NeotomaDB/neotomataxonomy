__author__ = 'scottsfarley'
f = open("expanded_extra_2.csv", 'rU')
import csv
import requests
reader = csv.reader(f)
fout = open("expanded_with_num_sites.csv", 'w')
writer = csv.writer(fout, lineterminator="\n")
i= 0
for row in reader:
    endpoint = "http://apidev.neotomadb.org/v1/data/occurrences?nametype=base&taxonids=" + str(row[0])
    r = requests.get(endpoint)
    j = r.json()
    data = j['data']
    numSites = len(data)
    row.insert(3, numSites)
    writer.writerow(row)
    i += 1
    if i % 100 == 0:
        print i