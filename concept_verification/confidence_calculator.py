# last updated 2015-02-25 toby

# determine the confidence level of our concept extraction

# example:
#concept "cyclic amp" (CUI) was extracted from the text snipped "cAMP"
#for the text snipped "cAMP", two concepts were extracted:
#	1. cyclic AMP: extracted 1000 times
#	2. CAMP (peptide): extracted 10 times
#
#our confidence that "cAMP" refers to cyclic amp is:
#	1000/(1000+10) = 99.00%
#	as in, 99% of the time "cAMP" means the cyclic adenine monophosphate
#
#	and only 10/(1000+10) = 1% of the time does it mean the peptide
#
#therefore if our predication (subject, pred, object) is based on the
#concept cathelicidin peptide , using "cAMP", then we are only 1% confident
#that we extracted the right concept
from __future__ import division
import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file
from collections import defaultdict

def load_data():
	text_concept_counts = defaultdict(dict)
	text_concept_totals = defaultdict(int)

	cur_snippet = ""
	for line in read_file("text_to_concept_mappings_count.txt"):
		vals = line.split('|')
		if len(vals) == 1: # a text snippet
			cur_snippet = vals[0]
		else:
			assert len(vals) == 2
			cui = vals[0]
			num = int(vals[1])
			text_concept_counts[cur_snippet][cui] = num
			text_concept_totals[cur_snippet] += num

	return (text_concept_counts, text_concept_totals)

text_concept_counts, text_concept_totals = load_data()

def debug():
	for key, subdict in text_concept_counts.items():
		print key
		for cui, num in subdict.items():
			print cui, num

def confidence(concept_id, text_snippet):
	return text_concept_counts[text_snippet][concept_id] / text_concept_totals[text_snippet]
