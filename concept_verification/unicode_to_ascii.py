# last updated 2015-02-23 toby

import unicodedata

def convert_unicode_to_ascii(text):
	print text

	text = text.replace(u'\xb1', "+/-") # replace the plus minus symbol
	text = text.replace(u'\xb7', ".") # replace middle dot with period (pmid 20491765)

	text = unicodedata.normalize("NFKD", text) # do what we can...

	text = text.replace(u'\u0308', "") # delete the two dots on top

#	replace mu with micro (pmid 24626782, sid 155628315)
#	sometimes called "mu" instead of micro... what to do????
	text = text.replace(u'\u03bc', "micro")

#	replace sigma with sigma (pmid 24474250, sid 153797529)
	text = text.replace(u'\u03c3', "sigma")
	text = text.replace(u'\u03b2', "beta")

	text = text.replace(u'\u0301', "") # delete accent
	text = text.replace(u'\u03b1', "alpha")
	text = text.replace(u'\u2264', "</=") # pmid 24416322



	print "\ncleaned text---------------------------------"
	print text
	print "\n"

	return text.encode("ascii")
