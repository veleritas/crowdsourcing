# last updated 2015-02-28 toby
"""
Takes the already chosen data for display to CrowdFlower
and adds the remaining information necessary for upload.
"""
import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file
from web_util import add_tag

from highlight_concepts import highlight
from get_pubmed_abstract import get_abstract_information
from unicode_to_ascii import convert_unicode_to_ascii

from replacer import replacer
from itertools import islice

def format_abstract(target, formatted_sentence, title, abstract_chunks):
	print "target"
	print target





	times_sentence_found = 0

	found, result = replacer(target, formatted_sentence, title)

	times_sentence_found += found
	formatted_abstract = add_tag("div", "title", result)

	if abstract_chunks:
		for chunk in abstract_chunks:
			found, result = replacer(target, formatted_sentence, chunk)
			times_sentence_found += found
			formatted_abstract += add_tag("div", "abstract_subsection", result)

	assert times_sentence_found == 1, "{0}".format(times_sentence_found)
	return formatted_abstract

def main():
	header = ["chosen_concept", "sub_conf_score", "obj_conf_score",
		"pred_id", "sent_id", "pubmed_id",
		"s_cui", "predicate", "o_cui",
		"sub_text", "obj_text", "sentence",
		"key_concept",
		"formatted_sentence", "abstract_title", "formatted_abstract"]

	with open("final_data.tsv", "w") as out:
		out.write("{0}\n".format("\t".join(header)))

		for line in islice(read_file("chosen_data.txt"), 1, None):
			vals = line.split('|')
			assert len(vals) == 12

			sentence = vals[11]
			pred_id = vals[3]
			sent_id = vals[4]
			pmid = vals[5]

			print "pmid {0} sid {1}".format(pmid, sent_id)

			form_sent, s_text, o_text = highlight(sentence, pred_id, sent_id)

			assert s_text == vals[9], "text {0} vals[9] {1}".format(s_text, vals[9])
			assert o_text == vals[10], "text {0} vals[10] {1}".format(o_text, vals[10])

			if not form_sent: # can't highlight
				continue

			title, abstract_chunks = get_abstract_information(pmid)
			title = convert_unicode_to_ascii(title)

#			highlight the sentence
			formatted_abstract = format_abstract(sentence, form_sent,
				title, abstract_chunks)

#			highlight the remaining instances of the selected concept
			key_concept_text = vals[9 + ["sub", "obj"].index(vals[0])]

			res, formatted_abstract = replacer(key_concept_text,
				add_tag("span", "key_concept", key_concept_text),
				formatted_abstract)

#			provide identifier if we want to toggle visibility
			formatted_abstract = add_tag("div", "formatted_abstract", formatted_abstract,
				"pid {0} sid {1} pmid {2}".format(pred_id, sent_id, pmid))

#-------------------------------------------------------------------------------
			out.write("{0}".format("\t".join(vals)))
			out.write("\t{0}".format(key_concept_text))
			out.write("\t{0}".format(form_sent))
			out.write("\t{0}".format(title))
			out.write("\t{0}\n".format(formatted_abstract))

	print "Done"

if __name__ == "__main__":
	main()
