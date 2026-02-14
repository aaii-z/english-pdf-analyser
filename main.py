import sys
import os
from analyzer.extraction import PDFExtractor
from analyzer.nlp import NLPEngine
from analyzer.cefr import CEFRAnalyzer
from analyzer.pdf_writer import PDFWriter
from analyzer.definitions import DefinitionFetcher

def main(input_pdf, output_pdf):
    print(f"Processing {input_pdf}...")
    
    # Initialize components
    extractor = PDFExtractor(input_pdf)
    nlp_engine = NLPEngine()
    cefr_analyzer = CEFRAnalyzer() # Uses default dictionary for now
    def_fetcher = DefinitionFetcher()
    
    writer = PDFWriter(extractor.get_document())
    
    words_to_highlight = []
    glossary_entries = {}
    level_counts = {}

    # Process each page
    for page_num, page in enumerate(extractor.get_document()):
        # Get words with coordinates
        pdf_words = page.get_text("words") 
        # pdf_words structure: (x0, y0, x1, y1, "word", block_no, line_no, word_no)
        
        # Reconstruct text for NLP (preserving order)
        text_content = " ".join([w[4] for w in pdf_words])
        
        # NLP Processing
        # We need to map spaCy tokens back to pdf_words
        # This is an approximation: we assume sequential order matches
        # and we strip punctuation for matching if needed.
        
        # A better heuristic for alignment:
        # Track character position in text_content
        
        nlp_results = nlp_engine.process_text(text_content)
        
        # Alignment logic
        # We will iterate through pdf_words and try to find the corresponding nlp result
        # This is simplified. 
        
        # Let's try matching by simple iteration since we built text from words
        # But spaCy might split words differently or group them.
        # Fallback: simple word-by-word lookup if alignment fails or just iterate pdf_words
        
        # Simple word-by-word approach for v1 (Contextless lemmatization fallback)
        for w in pdf_words:
            rect = w[:4]
            text = w[4]
            
            # Simple clean
            clean_text = "".join(ch for ch in text if ch.isalpha())
            if not clean_text:
                continue
                
            # Quick lookup (context-free for now for robust highlighting)
            # In a real pipeline, we'd map the NLP tokens to these rects
            lemma = nlp_engine.nlp(clean_text)[0].lemma_
            level = cefr_analyzer.get_level(lemma)
            
            if level:
                color = cefr_analyzer.get_color_for_level(level)
                if color:
                    words_to_highlight.append({
                        "page": page_num,
                        "rect": rect,
                        "color": color
                    })
                    
                # Collect stats
                level_counts[level] = level_counts.get(level, 0) + 1
                
                # Collect glossary (only for B2 and above)
                if level in ["B2", "C1", "C2"]:
                     if lemma not in glossary_entries:
                         # Placeholder definition
                         glossary_entries[lemma] = {
                             "word": lemma,
                             "level": level,
                             "pos": nlp_engine.nlp(clean_text)[0].pos_, # Get POS from spaCy
                             "definition": def_fetcher.get_definition(lemma) or f"Definition not found for {lemma}"
                         }

    print(f"Found {len(words_to_highlight)} words to highlight.")
    
    # 1. Highlight
    writer.highlight_words(words_to_highlight)
    
    # 2. Generate attachments
    attachments = []
    
    if glossary_entries:
        print("Generating glossary...")
        glossary_list = sorted(glossary_entries.values(), key=lambda x: x['word'])
        glossary_path = writer.generate_glossary(glossary_list, "glossary_temp.pdf")
        attachments.append(glossary_path)
        
    if level_counts:
        print("Generating stats...")
        stats_path = writer.generate_stats_page(level_counts, "stats_temp.pdf")
        attachments.append(stats_path)
        
    # 3. Merge
    print(f"Saving to {output_pdf}...")
    writer.merge_pdfs(input_pdf, attachments, output_pdf)
    
    # Cleanup
    for p in attachments:
        if os.path.exists(p):
            os.remove(p)
            
    print("Done!")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py <input_pdf> <output_pdf>")
    else:
        main(sys.argv[1], sys.argv[2])
