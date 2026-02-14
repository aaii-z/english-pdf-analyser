import pymupdf

def verify_output(path):
    doc = pymupdf.open(path)
    print(f"Total pages: {len(doc)}")
    
    # 1. Check annotations on page 0
    page0 = doc[0]
    annots = list(page0.annots())
    print(f"Page 0 annotations: {len(annots)}")
    if annots:
        print("First annotation color:", annots[0].colors['stroke'])
        
    # 2. Check for Glossary
    # Glossary should be on a later page (page 1 potentially, if sample is 1 page)
    # We search for "Glossary" text
    found_glossary = False
    for i in range(1, len(doc)):
        text = doc[i].get_text()
        if "Glossary" in text:
            print(f"Found Glossary on page {i}")
            found_glossary = True
            break
            
    # 3. Check for Stats
    found_stats = False
    for i in range(1, len(doc)):
        text = doc[i].get_text()
        if "Vocabulary Statistics" in text:
            print(f"Found Statistics on page {i}")
            found_stats = True
            break
            
    if found_glossary and found_stats and len(annots) > 0:
        print("Verification SUCCESS")
    else:
        print("Verification FAILED")

if __name__ == "__main__":
    verify_output("output.pdf")
