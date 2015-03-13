# last updated 2015-03-11 toby
"""
Generates the work units for CrowdFlower.
"""
import sys
sys.path.append("/home/toby/global_util/")
from file_util import read_file
from itertools import islice
from concept_finder import get_EUADR_concepts

sys.path.append("/home/toby/crowdsourcing/concept_verification/")
from get_pubmed_abstract import get_abstract_information
from unicode_to_ascii import convert_unicode_to_ascii

import nltk
from itertools import combinations
from web_util import add_tag

def find_concepts(sentence, concepts, semtype):
	return ([(concept, semtype[concept])
		for concept in concepts if concept in sentence])

def make_pairs(concepts):
	"""
	Generator for concept pairs of different semtypes.
	"""
	for sub, obj in combinations(concepts, 2):
		if sub[1] != obj[1]:
			yield (sub, obj)

def all_abstracts(concepts):
	"""
	Generator for tokenized abstracts and titles for every paper in
	the EU-ADR gold standard.
	"""
	sent_detector = nltk.data.load("tokenizers/punkt/english.pickle")
	for pmid in islice(read_file("all_EUADR_pmids.txt"), 1, None):
		title, abstract_chunks = get_abstract_information(pmid)
#		all snippets are guaranteed to be somewhere in title or text

		print "pmid:", pmid
		print title
		print concepts[pmid]

#		may want to tweak the sentence tokenizer
		abstract_fragments = ([sent_detector.tokenize(chunk)
			for chunk in abstract_chunks])

		print "***************"
		for chunks in abstract_fragments:
			print "\n\n".join(chunks)
		print "#################"

		yield (pmid, title, abstract_chunks, abstract_fragments)

def format_abstract(title, abstract_chunks, sentence, sub, obj):
#	highlight the subject and object last, across the entire abstract
	form_sent = add_tag("span", "orig_sentence", sentence)

	title = title.replace(sentence, form_sent)

	formatted_abstract = add_tag("div", "abstract_title", title)

	if abstract_chunks:
		for chunk in abstract_chunks:
			chunk = chunk.replace(sentence, form_sent)

			formatted_abstract += add_tag("div", "abstract_subsection", chunk)

#	highlight the terms
	formatted_abstract = formatted_abstract.replace(sub, add_tag("span", "subject_text", sub))
	formatted_abstract = formatted_abstract.replace(obj, add_tag("span", "object_text", obj))

#	wrap everything
	return add_tag("div", "formatted_abstract", formatted_abstract)

def relationship(all_relations, pmid, sub, obj):
#	pmid: 17244684
#	first sentence of abstract
#	gold std linked "GVHD" and "oral beclomethasone dipropionate"
#	and "gastrointestinal graft-versus host disease" with "BDP"
#	but never used "GVHD" with "BDP" even though they are the same thing

#	i'm going to stick to the gold std terms, and skip the links where
#	the gold std uses diff terms

	if (pmid, sub, obj) not in all_relations and (pmid, obj, sub) not in all_relations:
		return False

#	check that there is only one ordering
	assert ((pmid, sub, obj) in all_relations) ^ ((pmid, obj, sub) in all_relations)

	if (pmid, sub, obj) in all_relations:
		return all_relations[(pmid, sub, obj)]

	return all_relations[(pmid, obj, sub)]

def main():
	concepts, semtype, relation_type = get_EUADR_concepts()

	header = (["pubmed_id", "true_relation_type",
		"subject_text", "subject_type", "object_text", "object_type",
		"orig_sentence", "formatted_abstract"]
	)
	with open("out.txt", "w") as out:
		out.write("{0}\n".format("\t".join(header)))
		for pmid, title, abstract_chunks, abstract_fragments in all_abstracts(concepts):
			for chunk in abstract_fragments:
				for sentence in chunk:
					print sentence
					found_concepts = find_concepts(sentence, concepts[pmid], semtype)
					print found_concepts
#					a = raw_input()

					for sub, obj in make_pairs(found_concepts):
						form_abstract = format_abstract(title, abstract_chunks, sentence, sub[0], obj[0])

						rel_type = relationship(relation_type, pmid, sub[0], obj[0])
						if not rel_type:
							continue

						out.write("{0}\t".format(pmid))
						out.write("{0}\t".format(rel_type))
						out.write("{0}\t{1}\t".format(sub[0], sub[1]))
						out.write("{0}\t{1}\t".format(obj[0], obj[1]))
						out.write("{0}\t{1}\n".format(sentence, form_abstract))


#			a = raw_input()

if __name__ == "__main__":
	main()
