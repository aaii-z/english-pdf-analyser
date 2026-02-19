import requests
import time
import nltk
from nltk.corpus import wordnet

# Download WordNet data on first use (no-op if already downloaded)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)


class DefinitionFetcher:
    def __init__(self):
        self.api_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
        self.cache = {}

    def _from_wordnet(self, word):
        """Look up definition in WordNet (offline, very fast)."""
        synsets = wordnet.synsets(word)
        if synsets:
            return synsets[0].definition()
        return None

    def _from_api(self, word):
        """Fallback to free dictionary API for words WordNet doesn't cover."""
        try:
            response = requests.get(f"{self.api_url}{word}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    for meaning in data[0].get("meanings", []):
                        definitions = meaning.get("definitions", [])
                        if definitions:
                            time.sleep(0.1)
                            return definitions[0].get("definition")
        except Exception as e:
            print(f"Error fetching definition for {word}: {e}")
        return None

    def get_definition(self, word):
        """
        Returns the definition of a word.
        Tries WordNet first (offline), then falls back to the free dictionary API.
        """
        if word in self.cache:
            return self.cache[word]

        definition = self._from_wordnet(word) or self._from_api(word)
        self.cache[word] = definition
        return definition
