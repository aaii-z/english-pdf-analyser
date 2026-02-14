import requests
import time

class DefinitionFetcher:
    def __init__(self):
        self.api_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
        self.cache = {}

    def get_definition(self, word):
        """
        Fetches the definition of a word.
        Returns a string definition or None if not found.
        """
        if word in self.cache:
            return self.cache[word]

        try:
            response = requests.get(f"{self.api_url}{word}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                # Parse the first definition from the first meaning
                if isinstance(data, list) and len(data) > 0:
                    meanings = data[0].get("meanings", [])
                    for meaning in meanings:
                        definitions = meaning.get("definitions", [])
                        if definitions:
                            definition = definitions[0].get("definition")
                            self.cache[word] = definition
                            # Be nice to the API
                            time.sleep(0.1) 
                            return definition
        except Exception as e:
            print(f"Error fetching definition for {word}: {e}")
        
        self.cache[word] = None
        return None
