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
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import re
from pathlib import Path
import html

def clean_text(text):
    """Clean and format text for PDF rendering"""
    # Remove emoji characters (they don't render well in PDFs)
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "]+", flags=re.UNICODE)
    text = emoji_pattern.sub('', text)
    
    # Convert markdown bold (**text**) to HTML bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    
    # Convert markdown links [text](url) to just text (or keep url)
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'\1', text)
    
    # Escape XML special characters
    text = html.escape(text, quote=False)
    # Restore our bold tags
    text = text.replace('&lt;b&gt;', '<b>').replace('&lt;/b&gt;', '</b>')
    
    return text.strip()

def read_markdown(file_path):
    """Read markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def create_pdf(output_path='Sourav_Resume.pdf'):
    """Create PDF from markdown content"""
    
    # Register Segoe UI font (Windows system font)
    try:
        # Try to register Segoe UI font family
        segoe_ui_path = 'C:/Windows/Fonts/segoeui.ttf'
        segoe_ui_bold_path = 'C:/Windows/Fonts/segoeuib.ttf'
        segoe_ui_italic_path = 'C:/Windows/Fonts/segoeuii.ttf'
        
        if Path(segoe_ui_path).exists():
            pdfmetrics.registerFont(TTFont('SegoeUI', segoe_ui_path))
            if Path(segoe_ui_bold_path).exists():
                pdfmetrics.registerFont(TTFont('SegoeUI-Bold', segoe_ui_bold_path))
            if Path(segoe_ui_italic_path).exists():
                pdfmetrics.registerFont(TTFont('SegoeUI-Italic', segoe_ui_italic_path))
            font_name = 'SegoeUI'
            font_bold = 'SegoeUI-Bold'
            font_italic = 'SegoeUI-Italic'
        else:
            # Fallback to default font
            font_name = 'Helvetica'
            font_bold = 'Helvetica-Bold'
            font_italic = 'Helvetica-Oblique'
    except Exception as e:
        print(f"Warning: Could not load Segoe UI font, using default: {e}")
        font_name = 'Helvetica'
        font_bold = 'Helvetica-Bold'
        font_italic = 'Helvetica-Oblique'
    
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
        fontName=font_bold,
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=6,
        alignment=TA_LEFT
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=14,
        textColor=colors.HexColor('#4a4a4a'),
        spaceAfter=12,
        alignment=TA_LEFT
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontName=font_bold,
        fontSize=14,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=6,
        spaceBefore=12,
        bold=True
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontName=font_bold,
        fontSize=12,
        textColor=colors.HexColor('#2a2a2a'),
        spaceAfter=4,
        spaceBefore=8,
        bold=True
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName=font_name,
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
                    Paragraph('Email: sobiswas@microsoft.com<br/>Phone: +91-9830436633<br/>LinkedIn: linkedin.com/in/souravdasbiswas', body_style)
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
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            i += 1
            
            if not line:
                continue
                
            # Section headers (## )
            if line.startswith('## **') and line.endswith('**'):
                heading_text = clean_text(line.replace('## **', '').replace('**', ''))
                story.append(Spacer(1, 0.15*inch))
                story.append(Paragraph(f'<b>{heading_text}</b>', heading_style))
                
            # Subsection headers (### )
            elif line.startswith('### **'):
                subheading_text = clean_text(line.replace('### **', '').replace('**', ''))
                story.append(Paragraph(f'<b>{subheading_text}</b>', subheading_style))
                
            # Bold subsections with emojis (like "🤖 AI & Machine Learning")
            elif line.startswith('### '):
                subheading_text = clean_text(line.replace('### ', ''))
                story.append(Paragraph(f'<b>{subheading_text}</b>', subheading_style))
                
            # Bullets with bold text
            elif line.startswith('* **') or line.startswith('- **'):
                bullet_text = clean_text(line[2:])  # Remove '* ' or '- '
                # Check if there are sub-bullets following
                sub_items = []
                while i < len(lines) and (lines[i].strip().startswith('    * ') or lines[i].strip().startswith('    - ')):
                    sub_item = clean_text(lines[i].strip()[6:])  # Remove '    * '
                    sub_items.append(f'&nbsp;&nbsp;&nbsp;&nbsp;• {sub_item}')
                    i += 1
                
                story.append(Paragraph(f'• {bullet_text}', body_style))
                for sub_item in sub_items:
                    story.append(Paragraph(sub_item, body_style))
                
            # Regular bullets
            elif line.startswith('* ') or line.startswith('- '):
                bullet_text = clean_text(line[2:])
                story.append(Paragraph(f'• {bullet_text}', body_style))
                
            # Italic date ranges
            elif line.startswith('*') and '|' in line:
                date_text = clean_text(line.strip('*'))
                story.append(Paragraph(f'<i>{date_text}</i>', body_style))
                
            # Regular paragraphs
            elif line and not line.startswith('#') and not line.startswith('<'):
                para_text = clean_text(line)
                story.append(Paragraph(para_text, body_style))
    
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
