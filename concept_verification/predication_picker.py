import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file

from collections import defaultdict
import random

def main():
	print "reading data"

	info = defaultdict(set)
	values = []
	for i, line in enumerate(read_file("sorted_predication_by_conf.txt")):
		vals = line.split('|')

		score = float(vals[0])

		pid = vals[1]
		sid = vals[2]
		pmid = vals[3]
		sub = vals[4]
		pred = vals[5]
		obj = vals[6]
		sent = vals[7]

		values.append((score, pid, sid, pmid, sub, pred, obj, sent))

#		info[(sub, pred, obj)].add((score, pid, sid, pmid, sent))

	print "choosing random values"

	N_DATA = 100
	DEPTH = 3
	count = defaultdict(set)
	chosen_ones = []

	print len(values)

	seen = set()
	while len(chosen_ones) < N_DATA:
		print len(chosen_ones)

		rand_data = random.choice(values)
		if rand_data in seen:
			print "seen before!!!!"
			continue

		seen.add(rand_data)


		score = rand_data[0]
		pid = rand_data[1]
		sid = rand_data[2]
		pmid = rand_data[3]
		sub = rand_data[4]
		pred = rand_data[5]
		obj = rand_data[6]

		print score
		print rand_data
		if score > 0.20:
			continue

		if len(count[(sub, pred, obj)]) < DEPTH:
			lol = (pid, sid, pmid)
			print count[(sub, pred, obj)]
			if lol not in count[(sub, pred, obj)]:
				print "adding"
				count[(sub, pred, obj)].add((pid, sid, pmid))
				chosen_ones.append(rand_data)

	with open("chosen_data.txt", "w") as out:
		for data in chosen_ones:
			out.write("{0}|{1}\n".format(data[0], "|".join(data[1:])))










if __name__ == "__main__":
	main()
