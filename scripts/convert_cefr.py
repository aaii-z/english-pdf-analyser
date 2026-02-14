import csv
import json
import os

def convert_csv_to_json(csv_path, json_path):
    cefr_dict = {}
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            headword = row['headword']
            # Headwords might have slashes, e.g. "a.m./A.M."
            # We should probably add all variants.
            
            # CEFR level
            level = row['CEFR']
            
            # Split by slash if present
            words = headword.split('/')
            for w in words:
                w = w.strip().lower()
                if w:
                    # Some duplicates might exist with different POS or levels
                    # For now, we overwrite or keep the "highest" or "lowest"?
                    # Let's just keep the first one we find, or maybe prioritize deeper logic later.
                    if w not in cefr_dict:
                        cefr_dict[w] = level
                        
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(cefr_dict, f, indent=2)
    
    print(f"Converted {len(cefr_dict)} words to {json_path}")

if __name__ == "__main__":
    convert_csv_to_json("data/cefrj.csv", "data/cefr_dict.json")
