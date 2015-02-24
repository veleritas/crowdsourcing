# last updated 2015-02-24 toby
import sys
sys.path.append("/home/toby/global_util/")
from convert import query_ncbi

import xml.etree.cElementTree as ET
from unicode_to_ascii import convert_unicode_to_ascii

def get_pubmed_article_xml_tree(pubmed_id):
	request = "efetch.fcgi?db=pubmed&id={0}&rettype=abstract".format(pubmed_id)
	response = query_ncbi(request)
	return ET.fromstring(response)

def parse_article_xml_tree(article_xml_tree):
	"""Returns title as a unicode string, and abstract as an Element"""
	for element in article_xml_tree.iter("ArticleTitle"):
		article_title = element.text
		break

	for element in article_xml_tree.iter():
		if element.tag == "Abstract":
			return (article_title, element)

	return (article_title, False) # no abstract, title only

def split_abstract(abstract_xml_tree):
	"""Splits an abstract XML tree into individual chunks, if they exist.

	Preserves the background/methods/etc format of some papers (eg pmid 24885308)
	"""

	abstract_chunks = []
	for child in abstract_xml_tree.iter("AbstractText"):
		section_name = child.get("Label")
		text = child.text

		if isinstance(text, unicode):
			text = convert_unicode_to_ascii(text)

		if section_name is not None:
			text = "{0}: {1}".format(section_name, text)

		abstract_chunks.append(text)

	return abstract_chunks

def get_abstract_information(pubmed_id):
	article_xml_tree = get_pubmed_article_xml_tree(pubmed_id)
	title, abstract_xml_tree = parse_article_xml_tree(article_xml_tree)

	if abstract_xml_tree:
		return (title, split_abstract(abstract_xml_tree))

	return (title, [])

def main():
#	unit tests:
	tests = ["25696805", "17284678", "24885308", "22417663",
		"21269880", "2491759", "17360108", "11330043"]

	for pmid in tests:
		title, abstract = get_abstract_information(pmid)
		print title
		print abstract

if __name__ == "__main__":
	main()
