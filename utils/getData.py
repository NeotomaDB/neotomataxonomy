import requests
import csv
allData = requests.get("http://api.neotomadb.org/v1/dbtables/taxa?limit=50000&fields=taxonname,taxonid,highertaxonid").json()
fout = open("/Users/scottsfarley/documents/neotomataxonomy/short.csv", 'w')
writer = csv.DictWriter(fout, fieldnames=['Parent', 'Id', 'Name'], lineterminator="\n")
taxa = allData['data']
newData = []
for item in taxa:
    newItem = {
        'Parent': item['HigherTaxonID'],
        'Id' : item['TaxonID'],
        'Name' : item['TaxonName'].encode("utf8")
    }
    try:
        writer.writerow(newItem)
    except:
        pass
