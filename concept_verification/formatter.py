# last updated 2015-02-24 toby

# ask if the extracted concept mappings are correct

import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file
from web_util import add_tag

from highlight import highlight
from get_pubmed_abstract import get_abstract_information
from unicode_to_ascii import convert_unicode_to_ascii

from replacer import replacer

def format_abstract(target, formatted_sentence, title, abstract_chunks):
	times_found = 0

	found, result = replacer(target, formatted_sentence, title)

	times_found += found
	formatted_abstract = add_tag("div", "title", result)

	if abstract_chunks:
		for chunk in abstract_chunks:
			found, result = replacer(target, formatted_sentence, chunk)
			times_found += found
			formatted_abstract += add_tag("div", "abstract_subsection", result)

	assert times_found == 1, "We messed up in finding our sentence"
	return formatted_abstract

def main():
	print "starting"

	with open("./data/final_data.tsv", "w") as out:
		temp = ["pred_id", "sentence_id", "pubmed_id"]
		temp += ["gene_id", "predicate", "disease_cui", "sentence"]

		temp += ["formatted_sentence", "subject_text"]
		temp += ["abstract_title", "formatted_abstract"]

		out.write("{0}\n".format("\t".join(temp)))

		print "reading"
		for line in read_file("./data/almost_final_info.txt"):
			vals = line.split('|')

			print vals[0]

			assert len(vals) == 7
			pid = vals[0]
			sid = vals[1]
			pmid = vals[2]

			sub = vals[3]
			pred = vals[4]
			obj = vals[5]
			sent = vals[6]

			form_sent, sub_text, obj_text = highlight(sent, pid, sid)
			if not form_sent:
				continue

			print "all good"

#			info
			out.write("{0}".format("\t".join(vals)))

			out.write("\t{0}".format(form_sent))

			out.write("\t{0}".format(sub_text))

#			formatted abstract
			print "sid", sid
			print "pmid:", pmid

			title, abstract_chunks = get_abstract_information(pmid)

			title = convert_unicode_to_ascii(title)

			out.write("\t{0}".format(title))

			formatted_abstract = format_abstract(sent, form_sent, title, abstract_chunks)
			formatted_abstract = add_tag("div", "formatted_abstract", formatted_abstract,
				"pid {0} sid {1} pmid {2}".format(pid, sid, pmid), "none")

			out.write("\t{0}\n".format(formatted_abstract))
			print formatted_abstract

	print "done"

if __name__ == "__main__":
	main()
