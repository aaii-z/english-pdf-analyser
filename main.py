import sys
import os
from analyzer.extraction import PDFExtractor
from analyzer.nlp import NLPEngine
from analyzer.cefr import CEFRAnalyzer
from analyzer.pdf_writer import PDFWriter
from analyzer.definitions import DefinitionFetcher

import argparse

def main():
    parser = argparse.ArgumentParser(description="Analyze vocabulary in a PDF based on CEFR levels.")
    parser.add_argument("input_pdf", help="Path to input PDF file")
    parser.add_argument("output_pdf", help="Path to output PDF file")
    parser.add_argument("--levels", nargs="+", 
                        default=["A1", "A2", "B1", "B2", "C1", "C2"],
                        choices=["A1", "A2", "B1", "B2", "C1", "C2"],
                        help="CEFR levels to highlight and include (default: all)")
    parser.add_argument("--include-definitions", action="store_true",
                        help="Fetch and include definitions in the glossary")
    parser.add_argument("--estimate", action="store_true",
                        help="Enable frequency-based CEFR estimation for unknown words")
    
    args = parser.parse_args()
    
    input_pdf = args.input_pdf
    output_pdf = args.output_pdf
    target_levels = set([l.upper() for l in args.levels])
    
    print(f"Processing {input_pdf}...")
    print(f"Target levels: {', '.join(sorted(target_levels))}")
    
    # Initialize components
    extractor = PDFExtractor(input_pdf)
    nlp_engine = NLPEngine()
    cefr_analyzer = CEFRAnalyzer() # Uses default dictionary for now
    def_fetcher = DefinitionFetcher()
    
    writer = PDFWriter(extractor.get_document())
    
    words_to_highlight = []
    glossary_entries = {}
    level_counts = {}

    try:
        # Process each page
        for page_num, page in enumerate(extractor.get_document()):
            # Get words with coordinates
            pdf_words = page.get_text("words") 
            # pdf_words structure: (x0, y0, x1, y1, "word", block_no, line_no, word_no)
            
            # Reconstruct text for NLP (preserving order)
            text_content = " ".join([w[4] for w in pdf_words])
            
            nlp_results = nlp_engine.process_text(text_content)
            
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
                
                # Pass check_frequency based on flag
                level = cefr_analyzer.get_level(lemma, estimate=args.estimate)
                
                # Check if level is identified AND it is in the target list
                if level and level in target_levels:
                    color = cefr_analyzer.get_color_for_level(level)
                    if color:
                        words_to_highlight.append({
                            "page": page_num,
                            "rect": rect,
                            "color": color
                        })
                        
                    # Collect stats
                    level_counts[level] = level_counts.get(level, 0) + 1
                    
                    # Collect glossary (only for B2 and above, or strictly what requested?)
                    # User said "also be added in extra pages" implying the filter applies there too.
                    # Let's align glossary with target levels.
                    # Typically glossary is for harder words, but if user asks for A1, maybe they want A1 glossary?
                    # Let's include everything requested in glossary to be safe/flexible.
                    
                    if lemma not in glossary_entries:
                         entry = {
                             "word": lemma,
                             "level": level,
                             "pos": nlp_engine.nlp(clean_text)[0].pos_, # Get POS from spaCy
                         }
                         
                         if args.include_definitions:
                             entry["definition"] = def_fetcher.get_definition(lemma) or f"Definition not found for {lemma}"
                             
                         glossary_entries[lemma] = entry

        print(f"Found {len(words_to_highlight)} words to highlight from levels {target_levels}.")
        
        # 1. Highlight
        writer.highlight_words(words_to_highlight)
        
        # 2. Generate attachments
        attachments = []
        
        if glossary_entries:
            print(f"Generating glossary with {len(glossary_entries)} entries...")
            glossary_list = sorted(glossary_entries.values(), key=lambda x: x['word'])
            glossary_path = writer.generate_glossary(glossary_list, "glossary_temp.pdf")
            attachments.append(glossary_path)
        else:
            print("No glossary entries generated (maybe no words matches the selected levels).")
            
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

    finally:
        # Ensure we close the doc if something crashes, though PyMuPDF is robust
        pass

if __name__ == "__main__":
    main()
