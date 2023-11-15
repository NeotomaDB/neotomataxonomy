__author__ = 'scottsfarley'

import csv
import requests

# Call the Neotoma API:
url = "http://api.neotomadb.org/v2.0/data/taxa?limit=50000&taxagroupid=vpl"
json = requests.get(url, timeout = 2000).json()
taxa = json['data']

# Set up the output file:
fout = open("./data/expanded_extra_2.csv", 'w')
writer = csv.writer(fout, lineterminator="\n")

# Define the root variables we're interested in.
stops = ['Bacteria', 'Archaea', 'Protozoa', 'Chromista', 'Plantae', 'Fungi', 'Animalia', 'Algae']
stopIDs = [30, 63, 1414]


def getTaxonInfo(taxonid, tax):
    """_Create the recursive taxon path for an individual taxon._

    Args:
        taxonid (_integer_): _The (Neotoma) taxon ID for a particular taxon_
        tax (_list_): _A list of taxonnames for the node path a particular taxon takes to the root._

    Returns:
        _list_: _A set of taxonomic names relating the focal taxon to the root of the tree._
    """
    # Use a generator expression to return the right object:
    target = next((item for item in taxa if item.get("taxonid") == taxonid), None)
    if target is None:
        tax.append("Other")
        return tax
    elif target['taxonname'] in stops:
        tax.append(target['taxonname'].encode("utf8"))
        return tax
    elif target['taxonid'] in stopIDs or target['highertaxonid'] is None or target['highertaxonid'] == taxonid:
        return tax
    else:
        tax.append(target['taxonname'].encode("utf8"))
        return getTaxonInfo(target['highertaxonid'], tax)

def getTaxonCount(taxonid):
    """_summary_

    Args:
        taxonid (_type_): _description_
    """
    endpoint = f"http://api.neotomadb.org/v2.0/data/sites?taxa={taxonid}&limit=99999"
    json = requests.get(endpoint, timeout = 2000).json()
    return len(json.get('data'))

total = len(taxa)
i = 0

for taxon in taxa:
    print(i, total)
    i += 1
    thistaxonid = taxon['taxonid']
    taxonomy = getTaxonInfo(thistaxonid, [])
    taxonomy.reverse()
    author = taxon['author']
    try:
        author = author.encode('utf8')
    except Exception as e:
        author = "unknown"
    taxonomy.insert(0, getTaxonCount(taxon['taxonid']))
    taxonomy.insert(0, author)
    taxonomy.insert(0, taxon['status'] == 'extinct')
    taxonomy.insert(0, thistaxonid)
    writer.writerow(taxonomy)

