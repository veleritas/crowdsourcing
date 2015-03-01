# last updated 2015-02-28 toby
"""
Picks a set number of predications to give to the crowd.
This is mostly so that we keep our experiment within budget.
"""
import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file

import random
from itertools import islice
from collections import defaultdict

def main():
	print "Reading data"

	values = []
	for line in islice(read_file("predication_by_sub_conf.txt"), 1, None):
		vals = line.split('|')
#		sub_score, obj_score, pid, sid, pmid, s_cui, pred, o_cui, sub_text, obj_text, sent
		values.append(vals)

	print "Choosing random values"

	NUM_TASKS = 100
	DEPTH = 3
	CONFIDENCE_THRESHOLD = 0.2

	chosen_data = []
	count = defaultdict(set)
	balance = [0, 0] # number of subjects and objects chosen
	while len(chosen_data) < NUM_TASKS:
		print len(chosen_data)
		rand_data = random.choice(values)

		key_concept = random.choice([("sub", 0), ("obj", 1)])
#		check that we aren't confident
		if float(rand_data[key_concept[1]]) > CONFIDENCE_THRESHOLD:
			continue

		if balance[key_concept[1]] >= (NUM_TASKS / 2):
			continue

		balance[key_concept[1]] += 1

		pid = rand_data[2]
		sid = rand_data[3]
		pmid = rand_data[4]

		s_cui = rand_data[5]
		pred = rand_data[6]
		o_cui = rand_data[7]

		triple = (s_cui, pred, o_cui)
		if len(count[triple]) >= DEPTH:
			continue

		info = (key_concept[0], pid, sid, pmid)
		if info not in count[triple]:
			count[triple].add(info)
			chosen_data.append([key_concept[0]] + rand_data)

	header = ["chosen_concept", "sub_conf_score", "obj_conf_score",
		"pred_id", "sent_id", "pubmed_id",
		"s_cui", "predicate", "o_cui",
		"sub_text", "obj_text", "sentence"]

	with open("chosen_data.txt", "w") as out:
		out.write("{0}\n".format("|".join(header)))
		for data in chosen_data:
			out.write("{0}\n".format("|".join(data)))

if __name__ == "__main__":
	main()
