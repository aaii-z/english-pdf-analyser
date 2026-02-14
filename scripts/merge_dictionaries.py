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

def load_academic_json(json_path, default_level):
    data = {}
    if not os.path.exists(json_path):
        print(f"File not found: {json_path}")
        return data

    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            raw_data = json.load(f)
            # Structure: "word": { ... } or "word": [...]
            for word, content in raw_data.items():
                if word:
                    word = word.strip().lower()
                    data[word] = default_level
        except json.JSONDecodeError as e:
            print(f"Error reading JSON {json_path}: {e}")
    return data

def main():
    cefrj_path = "data/cefrj.csv"
    oxford_path = "data/oxford_5000.json"
    nawl_path = "data/nawl.json"
    avl_path = "data/avl.json"
    output_path = "data/cefr_dict.json"
    
    print("Loading CEFR-J...")
    cefrj_data = load_cefrj(cefrj_path)
    print(f"Loaded {len(cefrj_data)} words from CEFR-J.")
    
    print("Loading Oxford 5000...")
    oxford_data = load_oxford(oxford_path)
    print(f"Loaded {len(oxford_data)} words from Oxford 5000.")
    
    print("Loading NAWL (assigning C1)...")
    nawl_data = load_academic_json(nawl_path, "C1")
    print(f"Loaded {len(nawl_data)} words from NAWL.")

    print("Loading AVL (assigning C2)...")
    avl_data = load_academic_json(avl_path, "C2")
    print(f"Loaded {len(avl_data)} words from AVL.")

    print("Loading English 10k (ENGLISH_CERF_WORDS.csv)...")
    english10k_data = load_cefrj("data/ENGLISH_CERF_WORDS.csv") # Format seems identical to CEFR-J
    print(f"Loaded {len(english10k_data)} words from English 10k.")
    
    # Merge strategy:
    # 1. Start with CEFR-J
    # 2. Update with Oxford 5000 
    # 3. Update with English 10k (new source)
    # 4. Add NAWL only if not present 
    # 5. Add AVL only if not present
    
    merged_data = cefrj_data.copy()
    merged_data.update(oxford_data)
    merged_data.update(english10k_data) # Update with 10k list
    
    # Add NAWL
    for w, l in nawl_data.items():
        if w not in merged_data:
            merged_data[w] = l
            
    # Add AVL
    for w, l in avl_data.items():
        if w not in merged_data:
            merged_data[w] = l
    
    print(f"Total unique words after merge: {len(merged_data)}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=2)
        
    print(f"Saved merged dictionary to {output_path}")

if __name__ == "__main__":
    main()
