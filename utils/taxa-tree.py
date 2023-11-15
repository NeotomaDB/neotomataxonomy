__author__ = 'scottsfarley'
import requests
import csv

url = "http://api.neotomadb.org/v1/dbtables/taxa?limit=50000&taxagroupid=vpl&sort=taxonname"
json = requests.get(url).json()
taxa = json['data']

fout = open("/Users/scottsfarley/documents/neotomataxonomy/flat.tsv", 'w')
writer = csv.writer(fout, lineterminator="\n")
stops = ['Bacteria', 'Archaea', 'Protozoa', 'Chromista', 'Plantae', 'Fungi', 'Animalia', 'Algae']
stopIDs = [30, 63, 1414]
tree = {}



def getTaxonInfo(taxonID, tax):
    thisTaxon = None
    for item in taxa:
        if item['TaxonID'] == taxonID:
            thisTaxon = item
    tax.append( thisTaxon['TaxonName'].encode("utf8"))
    if thisTaxon is None or thisTaxon['TaxonName'] in stops:
        return tax
    elif thisTaxon['TaxonID'] in stopIDs or thisTaxon['TaxaGroupID'] == 'LAB':
        return tax
    else:
        getTaxonInfo(thisTaxon['HigherTaxonID'], tax)
        return tax


def getTaxonomy(taxonID):
    try:
        tax = []
        tax = getTaxonInfo(taxonID, tax)
        return tax
    except Exception as e:
        print str(e)
        return []

total = len(taxa)
i = 0
for taxon in taxa:
    print i, total
    i += 1
    thisTaxonID = taxon['TaxonID']
    taxonomy = getTaxonomy(thisTaxonID)
    taxonomy.append("Life")
    taxonomy.reverse()
    writer.writerow(taxonomy)
