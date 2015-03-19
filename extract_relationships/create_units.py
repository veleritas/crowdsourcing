# last updated 2015-03-19 toby
"""
Create work units for CrowdFlower.
Only focus on sentences, ignore the abstract.
"""
import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file
from string_util import remove_quotes
from itertools import islice
from web_util import add_tag
import random
from collections import defaultdict

def get_semtype(text):
	ans = [("SNP", "gene variant"), ("Genes", "gene or protein"),
		("Chemicals", "drug"), ("Diseases", "disease")]
	for prefix, semtype in ans:
		if text.startswith(prefix):
			return semtype

def format_word(text, entity):
	"""
	Format the key concepts to make them look nice. This saves me a
	lot of typing in the CrowdFlower interface.
	"""
	assert entity in ["sub", "obj"]
	if entity == "sub":
		return "&quot;{0}&quot;".format(add_tag("span", "subject_text", text))

	return "&quot;{0}&quot;".format(add_tag("span", "object_text", text))

def format_sentence(text, sub_text, obj_text):
	if text == sub_text:
		return add_tag("span", "subject_text", text)

	if text == obj_text:
		return add_tag("span", "object_text", text)

	return text


def pick_random_sentences(fname, loc):
	"""
	For a given file from the gold standard, this function generates
	a set number of work units randomly chosen from that file. The
	function chooses no more than NUM_PER_LINK_TYPE work units for each
	edge linking two different concept categories.

	Beware! This function loads the entire file into memory, and is
	therefore not very memory efficient.
	"""

	links = defaultdict(list)
	lines = [] # all the information for this file
	for i, line in enumerate(islice(read_file(fname, loc), 1, None)):
		vals = line.split('\t')
		vals = map(remove_quotes, vals)

#		convert semantic types for subject and object
		vals[6] = get_semtype(vals[6]) # sub
		vals[10] = get_semtype(vals[10]) # obj

		links[(vals[6], vals[10])].append(i)

		lines.append(line)


	NUM_PER_LINK_TYPE = 10 # number of CrowdFlower works units per link type
#	choose the work units, and yield them to our formatter function
	random.seed()
	for link_type, line_nums in links.items():
		if len(line_nums) < NUM_PER_LINK_TYPE:
			for val in line_nums:
				yield lines[val]
		else:
			chosen = set()
			while len(chosen) < NUM_PER_LINK_TYPE:
				chosen.add(random.choice(line_nums))

			for i in chosen:
				yield lines[i]

def main():
	header = ["pubmed_id", "true_relation_type",
		"subject_text", "subject_type", "subject_start", "subject_end",
		"object_text", "object_type", "object_start", "object_end",
		"formatted_sentence"]

	loc = "/home/toby/crowdsourcing/extract_relationships/gold_std/"
	files = ["EUADR_drug_disease.csv", "EUADR_drug_target.csv", "EUADR_target_disease.csv"]

	outfile = "deep_semantics_test_data.tsv"
	with open(outfile, "w") as out:
		out.write("{0}\n".format("\t".join(header)))
		for fname in files:
			for line in pick_random_sentences(fname, loc):
				vals = line.split('\t')
				vals = map(remove_quotes, vals)

				pmid = vals[1]
				true_type = vals[0]
				sentence = vals[11]
				sub_text = vals[3]
				obj_text = vals[7]

				s_start = int(vals[4])
				s_stop = int(vals[5])
				o_start = int(vals[8])
				o_stop = int(vals[9])
				sub_type = vals[6]

				obj_type = vals[10]

				assert sentence[s_start : s_stop] == sub_text
				assert sentence[o_start : o_stop] == obj_text

#			replace in sentence with highlight
				assert s_start > o_stop or o_start > s_stop

				positions = sorted([0, len(sentence), s_start, s_stop, o_start, o_stop])

				ans = []
				for i in range(len(positions)-1):
					ans += format_sentence(sentence[positions[i] : positions[i+1]], sub_text, obj_text)

				form_sentence = add_tag("div", "formatted_sentence", "".join(ans))

				out.write("{0}\t".format(pmid))
				out.write("{0}\t".format(true_type))

				out.write("{0}\t".format(format_word(sub_text, "sub")))
				out.write("{0}\t".format(get_semtype(sub_type)))
				out.write("{0}\t".format(s_start))
				out.write("{0}\t".format(s_stop))

				out.write("{0}\t".format(format_word(obj_text, "obj")))
				out.write("{0}\t".format(get_semtype(obj_type)))
				out.write("{0}\t".format(o_start))
				out.write("{0}\t".format(o_stop))

				out.write("{0}\n".format(form_sentence))

if __name__ == "__main__":
	main()
