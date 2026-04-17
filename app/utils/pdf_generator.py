from fpdf import FPDF
import logging

logger = logging.getLogger(__name__)

class MarketReportPDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 10, 'AI Market Analysis Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf(report_text: str) -> bytes:
    """
    Converts a Markdown-style report string into a PDF.
    """
    try:
        # Sanitize text to remove characters that standard PDF fonts can't handle (like emojis)
        sanitized_text = report_text.encode('latin-1', 'ignore').decode('latin-1')
        
        pdf = MarketReportPDF()
        pdf.add_page()
        pdf.set_font("helvetica", size=12)

        # Clean up some basic markdown markers for the PDF
        lines = sanitized_text.split('\n')
        for line in lines:
            if not line.strip():
                pdf.ln(2)
                continue
                
            if line.startswith('# '):
                pdf.set_font('helvetica', 'B', 16)
                pdf.cell(0, 10, line.replace('# ', '').strip(), ln=True)
                pdf.set_font('helvetica', size=12)
            elif line.startswith('## '):
                pdf.ln(3)
                pdf.set_font('helvetica', 'B', 14)
                pdf.cell(0, 10, line.replace('## ', '').strip(), ln=True)
                pdf.set_font('helvetica', size=12)
            elif line.startswith('- '):
                pdf.set_x(15)
                pdf.multi_cell(0, 10, f"* {line.replace('- ', '').strip()}")
            else:
                pdf.multi_cell(0, 10, line.strip())

        # Get PDF content as bytes
        return bytes(pdf.output())
    except Exception as e:
        logger.error(f"PDF Generation Error: {e}")
        return b""
