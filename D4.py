from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import *
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import io

# Define tabs globally so both functions can access it
TABS = {
    'health': ('🏋️', 13),      # Exercise icon -> page 14
    'finance': ('💰', 14),      # Money icon -> page 15
    'wellness': ('🧘', 15),     # Meditation icon -> page 16
    'nutrition': ('🥗', 16),    # Healthy food icon -> page 17
    'productivity': ('⏱️', 17), # Timer icon -> page 18
    'mental_health': ('🧠', 18),# Brain icon -> page 19
    'travel': ('✈️', 19),       # Airplane icon -> page 20
    'lifestyle': ('🏠', 20),    # House icon -> page 21
    'project': ('📊', 21)       # Chart icon -> page 22
}

def add_top_tabs(input_pdf="output_with_copies.pdf", output_pdf="output_with_tabs_top.pdf"):
    try:
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        # Get the dimensions from the first page
        first_page = reader.pages[0]
        width = float(first_page.mediabox.width)
        height = float(first_page.mediabox.height)

        # Define tab dimensions
        left_margin = 14.175  # 0.5 cm in points
        total_width = width / 2  # Half of page width
        tab_width = (total_width - left_margin) / 9  # Width for each tab
        tab_height = 25  # Same as side tabs

        # First, duplicate page 1 nine more times for the new sections
        page_to_duplicate = reader.pages[0]
        
        # Copy existing pages
        for page in reader.pages:
            writer.add_page(page)
            
        # Add 9 more copies of the first page
        for _ in range(9):
            writer.add_page(page_to_duplicate)

        # Now add annotations to all pages
        for page_num in range(len(writer.pages)):
            annotations = []
            # Create annotation for each tab
            for i, (tab_name, (icon, target_page)) in enumerate(TABS.items()):
                x_position = left_margin + (i * tab_width)
                
                # Create rectangle annotation (clickable area)
                rect = RectangleObject([
                    FloatObject(x_position),
                    FloatObject(height - tab_height),
                    FloatObject(x_position + tab_width),
                    FloatObject(height)
                ])
                
                # Create the destination array
                dest = ArrayObject([
                    NumberObject(target_page),
                    NameObject('/Fit'),
                ])

                # Create the action dictionary
                action = DictionaryObject()
                action.update({
                    NameObject('/Type'): NameObject('/Action'),
                    NameObject('/S'): NameObject('/GoTo'),
                    NameObject('/D'): dest
                })

                # Create the annotation dictionary
                annotation = DictionaryObject()
                annotation.update({
                    NameObject('/Type'): NameObject('/Annot'),
                    NameObject('/Subtype'): NameObject('/Link'),
                    NameObject('/Rect'): rect,
                    NameObject('/Border'): ArrayObject([NumberObject(0), NumberObject(0), NumberObject(0)]),
                    NameObject('/F'): NumberObject(4),
                    NameObject('/A'): action
                })
                
                annotations.append(annotation)

            # Add annotations to the page
            if annotations:
                if '/Annots' in writer.pages[page_num]:
                    current_annots = writer.pages[page_num]['/Annots']
                    current_annots.extend(annotations)
                else:
                    writer.pages[page_num][NameObject('/Annots')] = ArrayObject(annotations)

        # Write the output PDF
        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)
        
        print(f"Successfully created PDF with clickable top tabs: {output_pdf}")
        return True

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

def add_tab_visuals(input_pdf="output_with_tabs_top.pdf", output_pdf="final_output.pdf"):
    try:
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        # Get the dimensions
        first_page = reader.pages[0]
        width = float(first_page.mediabox.width)
        height = float(first_page.mediabox.height)

        # Create the template page with tabs
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=(width, height))

        # Define tab dimensions
        left_margin = 14.175  # 0.5 cm in points
        total_width = width / 2
        tab_width = (total_width - left_margin) / 9
        tab_height = 25

        # Define colors for tabs with stronger visibility
        tab_colors = [
            colors.HexColor('#FF69B4'),  # Health - Hot pink
            colors.HexColor('#32CD32'),  # Finance - Lime green
            colors.HexColor('#4169E1'),  # Wellness - Royal blue
            colors.HexColor('#9370DB'),  # Nutrition - Medium purple
            colors.HexColor('#DAA520'),  # Productivity - Goldenrod
            colors.HexColor('#9932CC'),  # Mental health - Dark orchid
            colors.HexColor('#FF6347'),  # Travel - Tomato
            colors.HexColor('#20B2AA'),  # Lifestyle - Light sea green
            colors.HexColor('#CD853F'),  # Project - Peru
        ]

        # Draw tabs and icons
        for i, (color, (tab_name, (icon, _))) in enumerate(zip(tab_colors, TABS.items())):
            x_position = left_margin + (i * tab_width)
            
            # Draw colored rectangle with border
            c.setFillColor(color)
            c.setStrokeColor(colors.black)
            c.setLineWidth(0.5)
            c.rect(x_position, height - tab_height, tab_width, tab_height, fill=1, stroke=1)
            
            # Add icon and text
            c.setFillColor(colors.white)  # White text for better contrast
            c.setFont("Helvetica-Bold", 8)  # Bold font for better visibility
            # Draw icon
            c.drawString(x_position + 5, height - tab_height/1.5, icon)
            # Draw text below icon
            text = tab_name[:8]  # Allow slightly longer text
            c.drawString(x_position + 2, height - tab_height + 5, text)

        c.save()
        packet.seek(0)

        # Create a new PDF with the tabs
        tab_pdf = PdfReader(packet)
        tab_page = tab_pdf.pages[0]

        # Merge tabs with each page
        for page in reader.pages:
            page.merge_page(tab_page)
            writer.add_page(page)

        # Save the result
        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

        print(f"Successfully created final PDF with visuals: {output_pdf}")
        return True

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    print("Adding clickable top tabs and visuals...")
    if add_top_tabs() and add_tab_visuals():
        print("Successfully created PDF with clickable top tabs and visuals!")
    else:
        print("Failed to modify the PDF. Please check if the input file is valid.")