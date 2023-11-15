import csv
import requests

allData = requests.get("https://api.neotomadb.org/v2.0/data/dbtables/taxa?limit=500000").json()
fout = open("./data/short.csv", 'w')
writer = csv.DictWriter(fout, fieldnames=['Parent', 'Id', 'Name'], lineterminator="\n")
taxa = allData['data']
newData = []
for item in taxa:
    newItem = {
        'Parent': item['highertaxonid'],
        'Id' : item['taxonid'],
        'Name' : item['taxonname'].encode("utf8")
    }
    try:
        writer.writerow(newItem)
    except Exception as e:
        print(e)
