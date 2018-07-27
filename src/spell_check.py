from enchant.checker import SpellChecker

def check_spelling(text):
	chkr = SpellChecker("en_US")
	chkr.set_text(text)
	for err in chkr:
		try:
			err.replace(chkr.suggest(err.word)[0])
		except Exception as e:
			pass
	correct_text = chkr.get_text()
	return correct_text