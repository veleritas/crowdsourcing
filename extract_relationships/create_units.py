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

def main():
	header = ["pubmed_id", "true_relation_type",
		"subject_text", "subject_type", "subject_start", "subject_end",
		"object_text", "object_type", "object_start", "object_end",
		"formatted_sentence"]

	loc = "/home/toby/crowdsourcing/extract_relationships/gold_std/"
	files = ["EUADR_drug_disease.csv", "EUADR_drug_target.csv", "EUADR_target_disease.csv"]
	with open("cf_no_abstract.tsv", "w") as out:
		out.write("{0}\n".format("\t".join(header)))
		for fname in files:
			for line in islice(read_file(fname, loc), 1, None):
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
