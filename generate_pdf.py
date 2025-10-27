"""
Generate PDF from README.md with proper formatting and working hyperlinks
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import re
from pathlib import Path


def convert_markdown_to_html(text):
    """Convert markdown to HTML while preserving links and replacing emojis with symbols"""
    
    # Comprehensive emoji replacements - including variations with and without selectors
    emoji_replacements = {
        # Email variations
        '📧': '[Email]',
        
        # Phone variations  
        '📞': '[Phone]',
        
        # Link variations
        '🔗': '[Link]',
        
        # Robot/AI variations (for AI & Machine Learning)
        '🤖': '»',
        
        # Cloud variations (with and without variation selector)
        '☁️': '»',  # Cloud with variation selector (U+2601 + U+FE0F)
        '☁': '»',   # Cloud without variation selector (U+2601 only)
        
        # Briefcase variations (for Professional Development)
        '💼': '»',
        
        # Additional common emojis that might appear
        '⚡': '»',   # Lightning bolt
        '🚀': '»',   # Rocket
        '💻': '»',   # Laptop
        '🔧': '»',   # Wrench/tools
        '📊': '»',   # Bar chart
        '🎯': '»',   # Target
        '🌟': '»',   # Star
        '✨': '»',   # Sparkles
    }
    
    # Apply emoji replacements with comprehensive matching
    for emoji, replacement in emoji_replacements.items():
        text = text.replace(emoji, replacement)
    
    # Handle remaining emojis with a more comprehensive pattern
    # This pattern covers most emoji ranges including:
    # - Emoticons, symbols, pictographs
    # - Transport and map symbols  
    # - Enclosed characters
    # - Various symbol ranges
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"  # dingbats
        u"\U000024C2-\U0001F251"  # enclosed characters
        u"\U0001F900-\U0001F9FF"  # supplemental symbols
        u"\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-A
        u"\U00002600-\U000026FF"  # miscellaneous symbols (includes ☁)
        u"\U0000FE00-\U0000FE0F"  # variation selectors
        u"\U0001F170-\U0001F251"  # enclosed ideographic supplement
        "]+", 
        flags=re.UNICODE
    )
    
    # Replace any remaining emojis with a generic symbol
    def emoji_fallback(match):
        """Fallback for unrecognized emojis"""
        return '•'  # Use bullet point as generic symbol
    
    text = emoji_pattern.sub(emoji_fallback, text)
    
    # Clean up any extra whitespace after emoji removal
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Convert markdown links [text](url) to HTML links <a href="url">text</a>
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" color="blue"><u>\1</u></a>', text)
    
    # Convert markdown bold to HTML bold
    text = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', text)
    
    return text


def setup_fonts():
    """Setup Segoe UI fonts"""
    try:
        segoe_path = 'C:/Windows/Fonts/segoeui.ttf'
        segoe_bold_path = 'C:/Windows/Fonts/segoeuib.ttf'
        segoe_italic_path = 'C:/Windows/Fonts/segoeuii.ttf'
        
        if Path(segoe_path).exists():
            pdfmetrics.registerFont(TTFont('SegoeUI', segoe_path))
            if Path(segoe_bold_path).exists():
                pdfmetrics.registerFont(TTFont('SegoeUI-Bold', segoe_bold_path))
            if Path(segoe_italic_path).exists():
                pdfmetrics.registerFont(TTFont('SegoeUI-Italic', segoe_italic_path))
            return 'SegoeUI', 'SegoeUI-Bold', 'SegoeUI-Italic'
    except:
        pass
    return 'Helvetica', 'Helvetica-Bold', 'Helvetica-Oblique'


def create_styles(font_name, font_bold, font_italic):
    """Create custom paragraph styles"""
    styles = {}
    
    styles['Title'] = ParagraphStyle(
        'Title',
        fontName=font_bold,
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=4,
        leading=28
    )
    
    styles['SectionHeading'] = ParagraphStyle(
        'SectionHeading',
        fontName=font_bold,
        fontSize=13,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=8,
        spaceBefore=16
    )
    
    styles['JobTitle'] = ParagraphStyle(
        'JobTitle',
        fontName=font_bold,
        fontSize=11,
        textColor=colors.HexColor('#2a2a2a'),
        spaceAfter=4,
        spaceBefore=10
    )
    
    styles['DateRange'] = ParagraphStyle(
        'DateRange',
        fontName=font_italic,
        fontSize=9,
        textColor=colors.HexColor('#5a5a5a'),
        spaceAfter=6
    )
    
    styles['Body'] = ParagraphStyle(
        'Body',
        fontName=font_name,
        fontSize=10,
        textColor=colors.HexColor('#3a3a3a'),
        spaceAfter=4,
        leading=13,
        alignment=TA_JUSTIFY
    )
    
    styles['Bullet'] = ParagraphStyle(
        'Bullet',
        fontName=font_name,
        fontSize=10,
        textColor=colors.HexColor('#3a3a3a'),
        spaceAfter=3,
        leading=13,
        leftIndent=12,
        bulletIndent=0
    )
    
    styles['SubBullet'] = ParagraphStyle(
        'SubBullet',
        fontName=font_name,
        fontSize=9,
        textColor=colors.HexColor('#4a4a4a'),
        spaceAfter=2,
        leading=12,
        leftIndent=36,
        bulletIndent=24
    )
    
    styles['CertSubsection'] = ParagraphStyle(
        'CertSubsection',
        fontName=font_bold,
        fontSize=11,
        textColor=colors.HexColor('#2a2a2a'),
        spaceAfter=6,
        spaceBefore=8
    )
    
    return styles


def read_and_parse_markdown():
    """Read and parse README.md"""
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections_raw = content.split('---\n\n')
    sections = []
    
    for section_text in sections_raw[1:]:  # Skip header table
        lines = section_text.strip().split('\n')
        section_title = None
        items = []
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Section heading (## **TEXT**)
            if line.startswith('## **'):
                section_title = line.replace('## **', '').replace('**', '').strip()
                i += 1
                continue
            
            # Job title (### **TEXT**)
            if line.startswith('### **'):
                job_title = convert_markdown_to_html(line.replace('### ', ''))
                items.append(('job_title', job_title))
                i += 1
                continue
            
            # Certification subsection (### TEXT with emoji)
            if line.startswith('### '):
                subsection = convert_markdown_to_html(line.replace('### ', ''))
                items.append(('cert_subsection', subsection))
                i += 1
                continue
            
            # Date range (*TEXT*)
            if line.startswith('*') and '|' in line:
                date_text = line.strip('*').strip()
                items.append(('date', date_text))
                i += 1
                continue
            
            # Main bullet (* TEXT or * **TEXT**)
            if line.startswith('* '):
                bullet_text = convert_markdown_to_html(line[2:])
                
                # Check for sub-bullets on next lines
                sub_bullets = []
                j = i + 1
                while j < len(lines):
                    next_line = lines[j]
                    # Check if it's a sub-bullet (starts with 4 spaces + *)
                    if next_line.startswith('    * ') or next_line.startswith('    - '):
                        sub_bullet_text = convert_markdown_to_html(next_line.strip()[2:])
                        sub_bullets.append(sub_bullet_text)
                        j += 1
                    else:
                        break
                
                items.append(('bullet', bullet_text, sub_bullets))
                i = j
                continue
            
            # Regular paragraph
            if line and not line.startswith('<') and not line.startswith('#'):
                para_text = convert_markdown_to_html(line)
                if para_text:
                    items.append(('paragraph', para_text))
            
            i += 1
        
        if section_title and items:
            sections.append({'title': section_title, 'items': items})
    
    return sections


def generate_pdf(output_path='Sourav_Resume.pdf'):
    """Generate PDF from parsed resume data"""
    
    # Setup fonts
    font_name, font_bold, font_italic = setup_fonts()
    
    # Create styles
    style_dict = create_styles(font_name, font_bold, font_italic)
    
    # Parse resume
    sections = read_and_parse_markdown()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    story = []
    
    # Add header with image
    img_path = Path('images/self/Me.jpg')
    if img_path.exists():
        try:
            img = Image(str(img_path), width=0.9*inch, height=0.9*inch)
            
            # Create name and title paragraph with proper spacing
            name_title = Paragraph('<b><font size=16>Sourav Das Biswas</font></b><br/><font size=11>Senior FastTrack Solution Architect</font>', style_dict['Title'])
            
            # Create contact info paragraph with proper spacing
            contact_info = Paragraph('<font size=9>[Email] <a href="mailto:sobiswas@microsoft.com" color="blue"><u>sobiswas@microsoft.com</u></a><br/>[Phone] +91-9830436633<br/>[Link] <a href="https://linkedin.com/in/souravdasbiswas" color="blue"><u>linkedin.com/in/souravdasbiswas</u></a></font>', style_dict['Body'])
            
            header_data = [[img, name_title, contact_info]]
            
            header_table = Table(header_data, colWidths=[1.0*inch, 3.2*inch, 2.3*inch], rowHeights=[0.9*inch])
            header_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (1, 0), 'LEFT'),
                ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ]))
            
            story.append(header_table)
            story.append(Spacer(1, 0.15*inch))
        except Exception as e:
            print(f"Error adding image: {e}")
    
    # Add sections
    for section in sections:
        # Section heading
        story.append(Spacer(1, 0.05*inch))
        story.append(Paragraph(f'<b>{section["title"]}</b>', style_dict['SectionHeading']))
        
        # Section items
        for item in section['items']:
            item_type = item[0]
            
            if item_type == 'job_title':
                story.append(Paragraph(item[1], style_dict['JobTitle']))
            
            elif item_type == 'cert_subsection':
                story.append(Paragraph(f'<b>{item[1]}</b>', style_dict['CertSubsection']))
            
            elif item_type == 'date':
                story.append(Paragraph(f'<i>{item[1]}</i>', style_dict['DateRange']))
            
            elif item_type == 'bullet':
                bullet_text = item[1]
                sub_bullets = item[2] if len(item) > 2 else []
                
                # Add main bullet
                story.append(Paragraph(f'• {bullet_text}', style_dict['Bullet']))
                
                # Add sub-bullets
                for sub_bullet in sub_bullets:
                    story.append(Paragraph(f'◦ {sub_bullet}', style_dict['SubBullet']))
            
            elif item_type == 'paragraph':
                story.append(Paragraph(item[1], style_dict['Body']))
    
    # Build PDF
    try:
        doc.build(story)
        print(f"✅ PDF created successfully: {output_path}")
        print(f"✅ Hyperlinks are clickable in the PDF")
        return True
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    generate_pdf()
