import pymupdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as ReportLabImage
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
import io

class PDFWriter:
    def __init__(self, doc):
        self.doc = doc

    def highlight_words(self, words_to_highlight):
        """
        words_to_highlight: List of dicts {page, rect, color}
        """
        for item in words_to_highlight:
            page = self.doc[item['page']]
            rect = item['rect']
            color = item['color']
            
            annot = page.add_highlight_annot(rect)
            annot.set_colors(stroke=color)
            annot.update()

    def generate_glossary(self, glossary_data, output_path="glossary.pdf"):
        """
        glossary_data: List of dicts {word, definition, level}
        """
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("Glossary", styles['Title']))
        story.append(Spacer(1, 12))

        for item in glossary_data:
            text = f"<b>{item['word']}</b> (<i>{item.get('pos','?')}</i>, {item['level']}): {item['definition']}"
            story.append(Paragraph(text, styles['Normal']))
            story.append(Spacer(1, 6))

        doc.build(story)
        return output_path

    def generate_stats_page(self, level_counts, output_path="stats.pdf"):
        """
        level_counts: Dict {level: count}
        """
        # Prepare data sorted by CEFR level
        cefr_order = ["A1", "A2", "B1", "B2", "C1", "C2"]
        # Filter levels that actually exist in the data and sort them
        levels = [lvl for lvl in cefr_order if lvl in level_counts]
        counts = [level_counts[lvl] for lvl in levels]
        
        # Color mapping (matching cefr.py)
        color_map = {
            "A1": '#ccffcc', "A2": '#99ff99',
            "B1": '#ffff99', "B2": '#ffcc66',
            "C1": '#ff9999', "C2": '#ff6666'
        }
        bar_colors = [color_map.get(lvl, '#cccccc') for lvl in levels]
        
        plt.figure(figsize=(6, 4))
        plt.bar(levels, counts, color=bar_colors)
        plt.title('Vocabulary Level Distribution')
        plt.xlabel('CEFR Level')
        plt.ylabel('Count')
        
        chart_buffer = io.BytesIO()
        plt.savefig(chart_buffer, format='png')
        plt.close()
        chart_buffer.seek(0)

        # Create PDF with chart
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("Vocabulary Statistics", styles['Title']))
        story.append(Spacer(1, 12))
        
        # Legend/Table
        data = [['Level', 'Count', 'Color']]
        colors_map = {
            "A1": "Light Green", "A2": "Green",
            "B1": "Light Yellow", "B2": "Orange",
            "C1": "Light Red", "C2": "Red"
        }
        
        for lvl in levels:
             data.append([lvl, level_counts.get(lvl,0), colors_map.get(lvl, "")])
             
        t = Table(data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(t)
        story.append(Spacer(1, 24))

        story.append(ReportLabImage(chart_buffer, width=400, height=300))
        
        doc.build(story)
        return output_path

    def merge_pdfs(self, original_pdf, attachments, output_path):
        """
        Merges the original (now highlighted) PDF with glossary and stats.
        """
        # Save current doc to a temporary file or buffer? 
        # Actually PyMuPDF doc is already open. We can insert pages from other PDFs.
        
        for attachment in attachments:
            src_doc = pymupdf.open(attachment)
            self.doc.insert_pdf(src_doc)
            src_doc.close()
            
        self.doc.save(output_path)
