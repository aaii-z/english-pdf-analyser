import json
import os
from wordfreq import zipf_frequency

class CEFRAnalyzer:
    def __init__(self, data_path="data/cefr_dict.json"):
        self.word_levels = {}
        if os.path.exists(data_path):
            self.load_data(data_path)
        else:
            # Fallback if file not found
            print(f"Warning: CEFR data file {data_path} not found. Using empty dict.")


    def load_data(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                self.word_levels = json.load(f)

    def get_level(self, word):
        """Returns the CEFR level of a word (lemma). Defaults to frequency estimation if not found."""
        level = self.word_levels.get(word.lower())
        if level:
            return level
        return self.estimate_level(word)

    def estimate_level(self, word):
        """Estimates CEFR level based on word frequency (Zipf scale)."""
        freq = zipf_frequency(word, 'en')
        
        if freq == 0:
            return None # Unknown word / Typos
            
        if freq > 6.0: return "A1"
        elif freq > 5.0: return "A2"
        elif freq > 4.0: return "B1"
        elif freq > 3.5: return "B2"
        elif freq > 3.0: return "C1"
        else: return "C2"

    def get_color_for_level(self, level):
        """Returns RGB tuple for a CEFR level."""
        colors = {
            "A1": (0.8, 1.0, 0.8), # Light Green
            "A2": (0.6, 1.0, 0.6), # Green
            "B1": (1.0, 1.0, 0.6), # Light Yellow
            "B2": (1.0, 0.8, 0.4), # Orange
            "C1": (1.0, 0.6, 0.6), # Light Red
            "C2": (1.0, 0.4, 0.4)  # Red
        }
        return colors.get(level, None)
