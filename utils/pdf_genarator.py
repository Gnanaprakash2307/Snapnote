from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os


def generate_pdf(title, content, output_dir="./exports"):
    """
    Generate a PDF file from text content
    """
    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Create output file path
        pdf_filename = f"{title.replace(' ', '_')}.pdf"
        pdf_path = os.path.join(output_dir, pdf_filename)

        # Create PDF document
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        styles = getSampleStyleSheet()

        # Create document content
        content_elements = []

        # Add title
        title_style = styles['Title']
        content_elements.append(Paragraph(title, title_style))
        content_elements.append(Spacer(1, 12))

        # Add content paragraphs
        normal_style = styles['Normal']
        paragraphs = content.split('\n\n')
        for paragraph in paragraphs:
            if paragraph.strip():
                content_elements.append(Paragraph(paragraph, normal_style))
                content_elements.append(Spacer(1, 6))

        # Build PDF
        doc.build(content_elements)

        return pdf_path
    except Exception as e:
        raise Exception(f"PDF generation error: {str(e)}")