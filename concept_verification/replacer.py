def replacer(target, substitute, source):
	"""Look for target in source.
	If found, replace target with substitute.
	Returns: (found or not, replaced string)
	"""

	found = source.count(target)

	if found == 0: # can't find target
		return (False, source)

	if found == 1:
		return (True, source.replace(target, substitute))

#	this should never happen
	raise Exception("Target is not unique in source!")
