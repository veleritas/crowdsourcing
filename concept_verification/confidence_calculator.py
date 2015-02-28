# last updated 2015-02-27 toby
"""
Determines the level of confidence of extracting a particular CUI
from a snippet of text.

Confidence is a float from 0 to 1 inclusive.

How confidence is calculated:
Imagine the text snipped "cAMP". This text snippet can map to the CUI
C0001455 and the Entrez gene ID 820. C0001455 has the semtypes: nnon
and bacs. Gene ID 820 just has the semtype of gngm. Therefore "cAMP"
has the semtypes: gngm, nnon, and bacs.

If we extracted gene ID 820 from "cAMP", the score is 1/3, because
"gngm" is one of the three possible semtypes for "cAMP". If we
extracted C0001455 from "cAMP", then the confidence score is 2/3
because the CUI has two of the three possible semtypes for "cAMP".

If a CUI was not extracted from a particular piece of text, then the
confidence score is zero.
"""

from __future__ import division

import sys
sys.path.append("/home/toby/global_util/semmeddb/")
from get_cui_semtypes import get_cui_semtypes
from get_text_to_cuis import get_text_to_cuis
from get_text_semtypes import get_text_semtypes

_cui_semtypes = get_cui_semtypes()
_text_to_cuis = get_text_to_cuis()
_text_semtypes = get_text_semtypes()

def confidence_score(cui, text_snippet):
#	text does not map to this CUI at all
	if cui not in _text_to_cuis[text_snippet]:
		return 0

	num = (sum(map(lambda semtype:
		semtype in _text_semtypes[text_snippet], _cui_semtypes[cui])))

	return num / len(_text_semtypes[text_snippet])
