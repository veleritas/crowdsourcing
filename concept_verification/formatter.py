# last updated 2015-02-23 toby

# ask if the extracted concept mappings are correct

import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file

from highlight import highlight
from highlight import add_span_tag
from get_pubmed_abstract import get_abstract_information
from unicode_to_ascii import convert_unicode_to_ascii
from searcher import replacer

def format_abstract(sentence, formatted_sentence, title, abstract_sentences):
#	look for semmed sentence in abstract

	ans = ""
	found = 0
	if sentence == title:
		ans += formatted_sentence
		found += 1
	else:
		ans += title

	if not abstract_sentences:
		assert found == 1
		return add_span_tag("abstract", ans)

	ans += "<br>"

	if isinstance(abstract_sentences[0], list):
		for i, chunk in enumerate(abstract_sentences):
			res = replacer(sentence, formatted_sentence, chunk)
			if res:
				ans += " ".join(res)
				found += 1
			else:
				ans += " ".join(chunk)

			if i != len(abstract_sentences)-1:
				ans += "<br>"

	else:
		res = replacer(sentence, formatted_sentence, abstract_sentences)
		if res:
			found += 1
			ans += " ".join(res)
		else:
			ans += " ".join(abstract_sentences)


	if found != 1:
		raise Exception("Could not find our sentence!!!")

	return add_span_tag("abstract", ans)

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

			title, abstract_sentences = get_abstract_information(pmid)

			title = convert_unicode_to_ascii(title)

			out.write("\t{0}".format(title))


			formatted_abstract = format_abstract(sent, form_sent, title, abstract_sentences)
			out.write("\t{0}\n".format(formatted_abstract))

	print "done"

if __name__ == "__main__":
	main()
