import csv
import json
import os

def load_cefrj(csv_path):
    data = {}
    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}")
        return data
        
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            headword = row['headword']
            level = row['CEFR']
            
            # Headwords might have slashes, e.g. "a.m./A.M."
            words = headword.split('/')
            for w in words:
                w = w.strip().lower()
                if w and w not in data:
                    data[w] = level.upper() # Ensure uppercase
    return data

def load_oxford(json_path):
    data = {}
    if not os.path.exists(json_path):
        print(f"File not found: {json_path}")
        return data

    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            raw_data = json.load(f)
            # Structure is "0": { "word": ..., "cefr": ... }
            for key, item in raw_data.items():
                word = item.get('word')
                cefr = item.get('cefr')
                
                if word and cefr:
                    word = word.strip().lower()
                    cefr = cefr.upper()
                    # Only take valid levels
                    if cefr in ["A1", "A2", "B1", "B2", "C1", "C2"]:
                        data[word] = cefr
                        
        except json.JSONDecodeError as e:
            print(f"Error reading JSON: {e}")
            
    return data

def main():
    cefrj_path = "data/cefrj.csv"
    oxford_path = "data/oxford_5000.json"
    output_path = "data/cefr_dict.json"
    
    print("Loading CEFR-J...")
    cefrj_data = load_cefrj(cefrj_path)
    print(f"Loaded {len(cefrj_data)} words from CEFR-J.")
    
    print("Loading Oxford 5000...")
    oxford_data = load_oxford(oxford_path)
    print(f"Loaded {len(oxford_data)} words from Oxford 5000.")
    
    # Merge: Start with CEFR-J, update with Oxford (assuming Oxford might be more "standard" or just additive)
    # Actually, let's prioritize Oxford for overlapping words if we trust it more?
    # Or just merge.
    merged_data = cefrj_data.copy()
    merged_data.update(oxford_data)
    
    print(f"Total unique words after merge: {len(merged_data)}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=2)
        
    print(f"Saved merged dictionary to {output_path}")

if __name__ == "__main__":
    main()
