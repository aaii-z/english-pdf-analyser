from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_sample_pdf(path):
    c = canvas.Canvas(path, pagesize=letter)
    
    text = """
    This is a sample document for vocabulary analysis.
    The implementation of this project utilizes complex algorithms to identify
    distinct words based on their CEFR levels.
    
    We use Python as our programming paradigm.
    The esoteric nature of some words might trigger the higher level classification.
    """
    
    text_object = c.beginText(40, 750)
    for line in text.split('\n'):
        text_object.textLine(line)
        
    c.drawText(text_object)
    c.save()

if __name__ == "__main__":
    create_sample_pdf("sample.pdf")
