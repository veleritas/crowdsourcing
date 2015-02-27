# last updated 2015-02-17 toby

# pick 50 unique random triples (s_cui, pred, o_cui) from semmed
# pick no more than 3 diff sentences supporting each triple

# use for crowdflower

import random

from collections import defaultdict
import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file

def main():
	cur_triple = ()
	all_triples = set()

	all_triples = set()
	info = defaultdict(set)

	for line in read_file("./data/triple_info.txt"):
		vals = line.split('|')
		if len(vals) == 3:
			cur_triple = (vals[0], vals[1], vals[2])
			all_triples.add(cur_triple)
		else:
			assert len(vals) == 4
			vals[0] = vals[0].lstrip('\t')

			info[cur_triple].add((vals[0], vals[1], vals[2], vals[3]))

	print len(all_triples)
	print sum([len(b) for a, b in info.items()])



	poss_bad_gids = set()
	for line in read_file("./data/poss_wrong_geneids.txt"):
		poss_bad_gids.add(line)




	t = list(all_triples)

	N_TRIPLES = 60
	DEPTH = 3 # no more than this number sentences per triple

	chosen_trips = set()
	while len(chosen_trips) < N_TRIPLES:
		rand_trip = random.choice(t)
		if rand_trip[0] in poss_bad_gids:
			chosen_trips.add(random.choice(t))

	assert len(chosen_trips) == N_TRIPLES
	print "assertion ok"

	chosen_sent = defaultdict(set)
	for trip in chosen_trips:
		if len(info[trip]) <= DEPTH:
			chosen_sent[trip] = info[trip]
		else:
			while len(chosen_sent[trip]) < DEPTH:
				chosen_sent[trip].add(random.choice(list(info[trip])))


	print "number sentences: {0}".format(sum(map(len, chosen_sent.values())))



	with open("./data/almost_final_info.txt", "w") as out:
		for trip, data in chosen_sent.items():
			for item in data:
#	geneID, pred, dCUI, pid, sid, pmid, sentence

				out.write("{0}".format("|".join(item[0:3])))

				out.write("|{0}".format("|".join(trip)))
				out.write("|{0}\n".format(item[3]))

if __name__ == "__main__":
	main()
