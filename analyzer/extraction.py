import pymupdf

class PDFExtractor:
    def __init__(self, pdf_path):
        self.doc = pymupdf.open(pdf_path)

    def extract_words(self):
        """
        Extracts words from the PDF.
        Returns a list of tuples: (page_num, word_text, rect)
        rect is the bounding box of the word.
        """
        extracted_data = []
        for page_num, page in enumerate(self.doc):
            # get_text("words") returns a list of items:
            # (x0, y0, x1, y1, "word", block_no, line_no, word_no)
            words = page.get_text("words")
            for w in words:
                rect = pymupdf.Rect(w[0], w[1], w[2], w[3])
                text = w[4]
                extracted_data.append({
                    "page": page_num,
                    "text": text,
                    "rect": rect
                })
        return extracted_data

    def get_document(self):
        return self.doc

    def close(self):
        self.doc.close()
