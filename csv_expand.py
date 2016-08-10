import csv
f = open("flat.csv", 'r')
reader =  csv.reader(f)
out = open("expanded.csv", 'w')
writer = csv.writer(out, lineterminator='\n')
for row in reader:
    newRow = row[0].split('_')
    writer.writerow(newRow)
