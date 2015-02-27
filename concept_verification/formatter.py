# last updated 2015-02-24 toby

# ask if the extracted concept mappings are correct

import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file
from web_util import add_tag

sys.path.append("/home/toby/crowdsourcing/concept_verification/")
from highlight_concepts import highlight
from get_pubmed_abstract import get_abstract_information
from unicode_to_ascii import convert_unicode_to_ascii

from replacer import replacer

import random

def format_abstract(target, formatted_sentence, title, abstract_chunks):
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
	print "starting"

	with open("final_data.tsv", "w") as out:
		temp = ["conf_score", "pred_id", "sentence_id", "pubmed_id"]
		temp += ["gene_id", "predicate", "disease_cui", "sentence"]

		temp += ["formatted_sentence", "key_concept"]
		temp += ["abstract_title", "formatted_abstract"]

		out.write("{0}\n".format("\t".join(temp)))

		print "reading"
		for line in read_file("chosen_data.txt"):
			vals = line.split('|')

			score = vals[0]
			pid = vals[1]
			sid = vals[2]
			pmid = vals[3]

			sub = vals[4]
			pred = vals[5]
			obj = vals[6]
			sent = vals[7]

			print sent, pid, sid

			form_sent, sub_text, obj_text = highlight(sent, pid, sid)
			if not form_sent:
				continue

			print "all good"

#			info
			out.write("{0}".format("\t".join(vals)))
			out.write("\t{0}".format(form_sent))
#			out.write("\t{0}".format(sub_text))

#			formatted abstract
			print "sid", sid
			print "pmid:", pmid

			title, abstract_chunks = get_abstract_information(pmid)

			title = convert_unicode_to_ascii(title)
			formatted_abstract = format_abstract(sent, form_sent, title, abstract_chunks)

			poss_concepts = ["subject", "object"]

			key_concept = random.choice(poss_concepts)
			key_concept = (sub_text if key_concept == "subject" else obj_text)

			out.write("\t{0}".format(key_concept))
			out.write("\t{0}".format(title))


			res, formatted_abstract = replacer(key_concept, add_tag("span", "key_concept", key_concept), formatted_abstract)

			formatted_abstract = add_tag("div", "formatted_abstract", formatted_abstract,
				"pid {0} sid {1} pmid {2}".format(pid, sid, pmid))

			out.write("\t{0}\n".format(formatted_abstract))

	print "done"

if __name__ == "__main__":
	main()
