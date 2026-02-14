import spacy

class NLPEngine:
    def __init__(self, model="en_core_web_sm"):
        try:
            self.nlp = spacy.load(model)
        except OSError:
            print(f"Model {model} not found. Please run 'python -m spacy download {model}'")
            raise

    def process_text(self, text):
        """
        Process text and return a list of dicts with word info.
        """
        doc = self.nlp(text)
        results = []
        for token in doc:
            if not token.is_alpha or token.is_stop:
                continue
                
            results.append({
                "text": token.text,
                "lemma": token.lemma_,
                "pos": token.pos_,
                "idx": token.idx, # Character offset
                "len": len(token.text)
            })
        return results
