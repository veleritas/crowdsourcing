# last updated 2015-02-25 toby

# ranks all of our predications and the sentences they come from
# by increasing order of confidence

from collections import defaultdict
import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file

from semmed_info import _query_semmed
from confidence_calculator import confidence
import logging

def get_subject_text(sentence_id, predication_id):
	print sentence_id, predication_id
	query = ("SELECT SUBJECT_TEXT "
		"FROM SENTENCE_PREDICATION "
		"WHERE SENTENCE_ID = %s "
		"AND PREDICATION_ID = %s LIMIT 1;")

	sub_text = _query_semmed(query, (sentence_id, predication_id))
	return sub_text

def main():

	logging.basicConfig(filename="errors.log", level=logging.DEBUG)
#	read all the predicate information

	print "reading predicate info"

	cur_triple = ()
	info = defaultdict(set)

	loc = "/home/toby/crowdsourcing/concept_verification/"
	for line in read_file(loc + "data/triple_info.txt"):
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

#	go through and calculate confidence levels
	print "calculating conf levels"
	ans = []
	for triple, supporting_data in info.items():
		gid = triple[0]
		for pid, sid, pmid, sentence in supporting_data:
			sub_text = get_subject_text(sid, pid)
			if sub_text == "NO_RESPONSE":
				logging.warning("no db subject text sid {0} pid {1}".format(sid, pid))
				continue

			if sub_text not in sentence:
				logging.warning("sub_text not in sentence sid {0} pid {1}".format(sid, pid))
				continue

			if not sub_text:
				logging.warning("sub_text is empty sid {0} pid {1}".format(sid, pid))
				continue


			conf_score = confidence(gid, sub_text)

			print conf_score
			ans.append((conf_score, pid, sid, pmid, gid, triple[1], triple[2], sentence))

	ans = sorted(ans, key = lambda x: x[0])
	with open("sorted_predication_by_conf.txt", "w") as out:
		for item in ans:
			score = item[0]
			vals = item[1:]
			out.write("{0}|{1}\n".format(score, "|".join(vals)))


if __name__ == "__main__":
	main()
