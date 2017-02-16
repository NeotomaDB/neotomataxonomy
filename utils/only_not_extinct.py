f = open("expanded_extra.csv", 'rU')
import csv
import requests
reader = csv.reader(f)
fout = open("only_not_extinct.csv", 'w')
writer = csv.writer(fout, lineterminator="\n")
for row in reader:
    if row[1] == 'FALSE':
        writer.writerow(row)


