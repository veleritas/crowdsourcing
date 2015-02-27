def replacer(target, substitute, source):
	"""Look for target in source.
	If found, replace target with substitute.
	Returns: (times found, replaced string)
	"""
	return (source.count(target), source.replace(target, substitute))
