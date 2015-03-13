# last updated 2015-03-09 toby
"""
Querys PubTator and gets their annotations for a PubMed ID.
"""
import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file
import requests
from itertools import islice

def query_pubtator(pmid):
	settings = {
#		"format": "BioC",
		"Gene": "1",
		"Chemical": "1",
		"Disease": "1",
		"Mutation": "1",
		"pmid": pmid
	}

	url = "http://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/PubTator/abstract_ann.cgi"
	resp = requests.get(url, params = settings)

	if resp.status_code == requests.codes.ok:
		return resp.text

	raise Exception("Error querying PubTator with PMID {0}".format(pmid))

def main():
	for pmid in islice(read_file("all_EUADR_pmids.txt"), 1, None):
		print pmid
		res = query_pubtator(pmid)
		with open("./data/" + pmid + ".txt", "w") as out:
			out.write("{0}\n".format(res))

if __name__ == "__main__":
	main()
