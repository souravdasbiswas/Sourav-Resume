"""
Generate PDF from README.md using markdown2 and reportlab
"""
import markdown2
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
import re
from pathlib import Path

def read_markdown(file_path):
    """Read markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def create_pdf(output_path='Sourav_Resume.pdf'):
    """Create PDF from markdown content"""
    
    # Read the markdown file
    md_content = read_markdown('README.md')
    
    # Create PDF
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Container for PDF elements
    story = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=6,
        alignment=TA_LEFT
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#4a4a4a'),
        spaceAfter=12,
        alignment=TA_LEFT
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=6,
        spaceBefore=12,
        bold=True
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#2a2a2a'),
        spaceAfter=4,
        spaceBefore=8,
        bold=True
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#3a3a3a'),
        spaceAfter=6,
        leading=14
    )
    
    # Header with name and contact
    # Add profile image if exists
    img_path = Path('images/self/Me.jpg')
    if img_path.exists():
        try:
            img = Image(str(img_path), width=0.8*inch, height=0.8*inch)
            
            # Create header table with image, name, and contact
            header_data = [
                [
                    img,
                    Paragraph('<b>Sourav Das Biswas</b><br/><font size=11>Senior FastTrack Solution Architect</font>', title_style),
                    Paragraph('📧 sobiswas@microsoft.com<br/>📞 +91-9830436633<br/>🔗 linkedin.com/in/souravdasbiswas', body_style)
                ]
            ]
            
            header_table = Table(header_data, colWidths=[1*inch, 3.5*inch, 2*inch])
            header_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (1, 0), 'LEFT'),
                ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ]))
            
            story.append(header_table)
            story.append(Spacer(1, 0.2*inch))
        except Exception as e:
            # If image fails, use text only
            story.append(Paragraph('<b>Sourav Das Biswas</b>', title_style))
            story.append(Paragraph('Senior FastTrack Solution Architect', subtitle_style))
            story.append(Spacer(1, 0.1*inch))
    else:
        story.append(Paragraph('<b>Sourav Das Biswas</b>', title_style))
        story.append(Paragraph('Senior FastTrack Solution Architect', subtitle_style))
        story.append(Spacer(1, 0.1*inch))
    
    # Parse sections
    sections = md_content.split('---\n\n')
    
    for section in sections[1:]:  # Skip the header section
        lines = section.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Section headers (## )
            if line.startswith('## **') and line.endswith('**'):
                heading_text = line.replace('## **', '').replace('**', '')
                story.append(Spacer(1, 0.15*inch))
                story.append(Paragraph(f'<b>{heading_text}</b>', heading_style))
                
            # Subsection headers (### )
            elif line.startswith('### **'):
                subheading_text = line.replace('### **', '').replace('**', '')
                story.append(Paragraph(f'<b>{subheading_text}</b>', subheading_style))
                
            # Bold subsections
            elif line.startswith('* **'):
                bullet_text = line[2:]  # Remove '* '
                story.append(Paragraph(bullet_text, body_style))
                
            # Regular bullets
            elif line.startswith('* ') or line.startswith('- '):
                bullet_text = '• ' + line[2:]
                story.append(Paragraph(bullet_text, body_style))
                
            # Italic date ranges
            elif line.startswith('*') and '|' in line:
                story.append(Paragraph(f'<i>{line}</i>', body_style))
                
            # Regular paragraphs
            elif line and not line.startswith('#') and not line.startswith('<'):
                story.append(Paragraph(line, body_style))
    
    # Build PDF
    try:
        doc.build(story)
        print(f"✅ PDF created successfully: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        return False

if __name__ == "__main__":
    create_pdf()
