import re

class SpecialCharactersRemover:
    def process(self, text):
        """Removes any character that is not a letter (a-z, A-Z) or a number (0-9) from the text."""
        return re.sub(r'[^a-zA-Z0-9]', '', text)
