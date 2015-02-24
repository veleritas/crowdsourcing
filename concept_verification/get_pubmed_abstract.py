# last updated 2015-02-23 toby
import sys
sys.path.append("/home/toby/global_util/")
from convert import query_ncbi

import xml.etree.cElementTree as ET
from nltk.tokenize import sent_tokenize
from unicode_to_ascii import convert_unicode_to_ascii

def get_pubmed_article_xml_tree(pubmed_id):
	request = "efetch.fcgi?db=pubmed&id={0}&rettype=abstract".format(pubmed_id)
	response = query_ncbi(request)
	return ET.fromstring(response)

def parse_article_xml_tree(article_xml_tree):
#	return the title as a string
#	return the abstract as an Element
	for element in article_xml_tree.iter("ArticleTitle"):
		article_title = element.text
		break

	has_abstract = False
	for element in article_xml_tree.iter():
		if element.tag == "Abstract":
			has_abstract = True
			break

	if has_abstract:
		for element in article_xml_tree.iter("Abstract"):
			return (article_title, element)
	else:
		return (article_title, False)

def split_abstract(abstract_xml_tree):
#	returns a single list with individual sentences of the abstract
#	if the abstract is one chunk, then the list contains no other lists
#	if the abstract had the background/methods/etc format (eg pmid 24885308)
#	then the result is a list of lists
#	so that i can format nicely for crowdflower

#	count number of abstract text fields
	num = 0
	for child in abstract_xml_tree:
		if child.tag == "AbstractText":
			num += 1

	if num == 1:
		abstract_text = abstract_xml_tree[0].text

		if isinstance(abstract_text, unicode):
			abstract_text = convert_unicode_to_ascii(abstract_text)

		return sent_tokenize(abstract_text)

#	otherwise deal with the stupid background/conclusion format
	abstract_sentences = []
	for child in abstract_xml_tree:
		if child.tag == "AbstractText":
			section_name = child.get("Label")

			text = child.text
			if isinstance(text, unicode):
				text = convert_unicode_to_ascii(text)

			sentences = sent_tokenize(text)
			sentences[0] = "{0}: {1}".format(section_name, sentences[0])

			abstract_sentences.append(sentences)

	return abstract_sentences

def get_abstract_information(pubmed_id):
	article_xml_tree = get_pubmed_article_xml_tree(pubmed_id)
	title, abstract_xml_tree = parse_article_xml_tree(article_xml_tree)

	if abstract_xml_tree != False:
		abstract_sentences = split_abstract(abstract_xml_tree)
		return (title, abstract_sentences)
	else: # no abstract
		return (title, [])

def main():
#	pmid = "25696805"
#	pmid = "17284678"
#	pmid = "24885308"

#	pmid = "22417663"
#	pmid = "21269880"
#	pmid = "2491759"
#	pmid = "17360108"
	pmid = "11330043"

	title, abstract_sentences = get_abstract_information(pmid)

	print "title:", title
	print "sentences:"
	for a in abstract_sentences:
		print a
		print "\n"

if __name__ == "__main__":
	main()
