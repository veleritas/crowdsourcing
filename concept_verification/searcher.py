# last updated 2015-02-24 toby

# version 2.0:
# use string in string to check if exists
# if exists, just use a = b.replace(c, d)
# this avoids splitting into sentences...
# this should be unique as well???

# check if unique: use a.count(b)









def replacer(target, formatted_sentence, sentences):
#	given a list of sentences (or mis-broken sentences)
#	looks for the target sentence by joining together sentence pieces

#	returns a list where the original sentence fragments have been replaced by
#	the formatted sentence we want to print

	prefix = -1
	suffix = -1
	inside = -1
#	i'm assuming that there is only one instance of our sentence
#	in the abstract
	for i, text in enumerate(sentences):
		if text == target: # we can get an exact match with one sentence
			sentences[i] = formatted_sentence
			return sentences
		elif target.startswith(text) or text.startswith(target):
			prefix = i
		elif target.endswith(text) or text.endswith(target):
			suffix = i
		elif target in text:
			inside = i

	if prefix != -1 and suffix != -1:
		assert prefix < suffix
#		check that the string matches
		assert target == " ".join(sentences[prefix : suffix + 1]), "couldn't join properly"

		ans = sentences[:prefix]
		ans.append(formatted_sentence)
		ans += sentences[suffix+1 : ]
		return ans


	if prefix != -1:
#		target is shorter than the full sentence
#		eg pmid 17360108, sid 103389760

#		split sentence into two...
		assert target.startswith(sentences[prefix]) or sentences[prefix].startswith(target)

#		target is smaller than our actual sentence
		assert len(target) < len(sentences[prefix])
		ans = sentences[: prefix]
		ans.append(formatted_sentence)

		ans.append(sentences[prefix][len(target):])
		ans += sentences[prefix+1 : ]


		return ans

	if suffix != -1:
#		target is the suffix of a sentence we split
#		pmid 11330043 sid 76006064

		assert len(target) < len(sentences[suffix])
		ans = sentence[: prefix]
		ans.append(sentences[prefix][:-len(target)])
		ans.append(formatted_sentence)
		ans += sentences[prefix+1 :]
		print ans
		assert 0 == 1
		return ans

	if inside != -1:
		assert target in sentences[inside]

		sentences[inside] = sentences[inside].replace(target, formatted_sentence)

		print sentences

		return sentences












	return [] # could not find the target
