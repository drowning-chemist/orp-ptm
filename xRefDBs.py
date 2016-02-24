from bioservices.picr import PICR
import csv

def getPDBAccess(p, uniprot):
	# contact PICR database
	res = p.getUPIForAccession(uniprot, ["PDB"])
	
	# determine number of PDB entries attached to protein
	entries = len(res.findAll('accession'))
	
	pdbList = []
	# if there are PDB entries attached to the protein, create list
	if(entries > 0):
		for access in res.findAll('accession'):
			pdbList.append(access.get_text())
	return entries, pdbList
		
def readPhosphoSite(fname):
	numEntry = []
	site = []
	with open(fname, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			numEntry.append(row[0])
			site.append(row[1])
	return numEntry, site

def writeXRefs(fname, uniprotList, sites, entriesList, pdbList):
	with open(fname, 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',', quotechar='|')
		for i in range(len(uniprotList)):
			writer.writerow([uniprotList[i], sites[i], entriesList[i], pdbList[i]])
			
def main(argv=None):
	# settings
	inFile = 'phosphoSite.csv'
	outFile = 'phosphoSite.xref.csv'
	
	# parse input file
	entries, sites = readPhosphoSite(inFile)
	
	# populate lists
	pdbList = []
	numEntries = []
	p = PICR()
	for entry in entries:
		num, pdb = getPDBAccess(p, entry)
		numEntries.append(num)
		pdbList.append("; ".join(pdb))
	
	# write file
	writeXRefs(outFile, entries, sites, numEntries, pdbList)
	
if __name__=="__main__":
	main()