# last updated 2015-03-11 toby
"""
Finds all of the concepts from the EU-ADR gold standard.
"""
import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file
from itertools import islice
from collections import defaultdict

sys.path.append("/home/toby/crowdsourcing/concept_verification/")
from unicode_to_ascii import convert_unicode_to_ascii

def remove_quotes(text):
	return text.strip('"')

def convert_to_ascii(text):
	return convert_unicode_to_ascii(text.decode("unicode-escape"))

def get_semtype(text):
	ans = [("SNP", "variant"), ("Genes", "gene"),
		("Chemicals", "drug"), ("Diseases", "disease")]
	for prefix, semtype in ans:
		if text.startswith(prefix):
			return semtype

def get_EUADR_concepts():
	files = ["drug_disease", "drug_target", "target_disease"]
	types = [("disease", "drug"), ("gene", "drug"), ("gene", "disease")]
#	(drug disease ok)
#	(drug target): need to change to gene/snp drug
#	target disease: need to change to gene/snp disease

	concepts = defaultdict(set) # all of the text snippets for each pmid
	semtype = dict() # the semantic type of each text snippet
	relationship = dict()

	for name, text_type in zip(files, types):
		loc = "/home/toby/crowdsourcing/extract_relationships/"
		fname = loc + "gold_std/EUADR_{0}.csv".format(name)

		for line in islice(read_file(fname), 1, None):
			vals = line.split('\t')
			assert len(vals) == 12
			vals = map(remove_quotes, vals)
			vals = map(convert_to_ascii, vals)

			relation_type = vals[0]
			pmid = vals[1]
			sub_text = vals[3]
			obj_text = vals[7]

			concepts[pmid].add(sub_text)
			concepts[pmid].add(obj_text)

			if sub_text in semtype:
				assert text_type[0] == semtype[sub_text]

			if obj_text in semtype:
				assert text_type[1] == semtype[obj_text]

			semtype[sub_text] = text_type[0]
			semtype[obj_text] = text_type[1]

			relationship[(pmid, sub_text, obj_text)] = relation_type

	return (concepts, semtype, relationship)

def main():
	print "hi"

if __name__ == "__main__":
	main()
