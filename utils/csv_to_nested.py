__author__ = 'scottsfarley'
import requests
url = "http://api.neotomadb.org/v1/dbtables/taxa?limit=50000&taxagroupid=vpl&sort=taxonname"
json = requests.get(url).json()
taxa = json['data']
import csv
fout = open("/Users/scottsfarley/documents/neotomataxonomy/expanded_extra_2.csv", 'w')
writer = csv.writer(fout, lineterminator="\n")

stops = ['Bacteria', 'Archaea', 'Protozoa', 'Chromista', 'Plantae', 'Fungi', 'Animalia', 'Algae']
stopIDs = [30, 63, 1414]
tree = {}

def getTaxonInfo(taxonID, tax):
    thisTaxon = None
    for item in taxa:
        if item['TaxonID'] == taxonID:
            thisTaxon = item
    tax.append(thisTaxon['TaxonName'].encode("utf8"))
    if thisTaxon['TaxonName'] in stops:
        return tax
    elif thisTaxon['TaxonID'] in stopIDs or thisTaxon['TaxaGroupID'] == 'LAB' or thisTaxon is None:
        tax.append("Other")
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
    taxonomy.reverse()
    author = taxon['Author']
    try:
        author = author.encode('utf8')
    except:
        author = "unknown"
    taxonomy.insert(0, author)
    taxonomy.insert(0, taxon['Extinct'])
    taxonomy.insert(0, thisTaxonID)
    writer.writerow(taxonomy)
    print taxonomy
