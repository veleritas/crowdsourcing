# last updated 2015-02-28 toby
"""
Ranks all predications that we might give to the crowd
based on the confidence of the concept extracted from
the source text.
"""
from collections import defaultdict
import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file
sys.path.append("/home/toby/global_util/semmeddb/")
from get_concept_source_text import get_concept_source_text

from confidence_calculator import confidence_score
import logging

def load_data():
	cur_triple = ()
	info = defaultdict(set)

	loc = "/home/toby/crowdsourcing/concept_verification/data/"
	for line in read_file("triple_info.txt", loc):
		line = line.lstrip('\t')
		vals = line.split('|')
		if len(vals) == 3:
			sub = vals[0]
			pred = vals[1]
			obj = vals[2]
			cur_triple = (sub, pred, obj)
		else:
			assert len(vals) == 4
			pid = vals[0]
			sid = vals[1]
			pmid = vals[2]
			sentence = vals[3]
			info[cur_triple].add((pid, sid, pmid, sentence))

	return info

def main():
	logging.basicConfig(filename = "ranking_errors.log", level = logging.DEBUG)

	print "Reading predicate info"
	info = load_data()

	print "Calculating confidence levels"
	ans = []
	for triple, supporting_data in info.items():
		s_cui = triple[0]
		o_cui = triple[2]
		for pid, sid, pmid, sentence in supporting_data:

			sub_text, obj_text = get_concept_source_text(sid, pid)

			if sub_text == "NO_RESPONSE" or obj_text == "NO_RESPONSE":
				logging.error("No entry for sid {0} pid {1} in sentence_predication".
					format(sid, pid))
				continue

			if not sub_text or not obj_text:
				logging.error("Empty text fields for sid {0} pid {1}".format(sid, pid))
				continue

			if (sub_text not in sentence) or (obj_text not in sentence):
				logging.error("Text not found in sentence sid {0} pid {1}".format(sid, pid))
				continue

			sub_conf_score = confidence_score(s_cui, sub_text)
			obj_conf_score = confidence_score(o_cui, obj_text)

			print sub_conf_score, obj_conf_score

			ans.append((sub_conf_score, obj_conf_score,
				pid, sid, pmid,
				s_cui, triple[1], o_cui, sub_text, obj_text, sentence))

#	print to file
	header = ["sub_conf_score", "obj_conf_score",
		"pred_id", "sent_id", "pubmed_id", "s_cui",
		"predicate", "o_cui", "sub_text", "obj_text", "sentence"]

	print "len ans", len(ans)
	ans = sorted(ans, key = lambda x: x[0])
	with open("predication_by_sub_conf.txt", "w") as out:
		out.write("{0}\n".format("|".join(header)))
		for item in ans:
			sub_score = item[0]
			obj_score = item[1]
			vals = item[2: ]
			out.write("{0}|{1}|{2}\n".format(sub_score, obj_score, "|".join(vals)))

	ans = sorted(ans, key = lambda x: x[1])
	with open("predication_by_obj_conf.txt", "w") as out:
		out.write("{0}\n".format("|".join(header)))
		for item in ans:
			sub_score = item[0]
			obj_score = item[1]
			vals = item[2: ]
			out.write("{0}|{1}|{2}\n".format(sub_score, obj_score, "|".join(vals)))


if __name__ == "__main__":
	main()
