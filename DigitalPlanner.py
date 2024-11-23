from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import io

def add_tabs_to_pdf(input_pdf="Golden spiral 2.pdf", output_pdf="output_with_tabs.pdf"):
    try:
        reader = PdfReader(input_pdf, strict=False)
        writer = PdfWriter()

        # Get the dimensions from the first page
        first_page = reader.pages[0]
        width = float(first_page.mediabox.width)
        height = float(first_page.mediabox.height)

        # Define colors for different months
        month_colors = {
            'JAN': colors.HexColor('#FFE4E1'),
            'FEB': colors.HexColor('#FFA07A'),
            'MAR': colors.HexColor('#FFDAB9'),
            'APR': colors.HexColor('#FFFFE0'),
            'MAY': colors.HexColor('#F0E68C'),
            'JUN': colors.HexColor('#98FB98'),
            'JUL': colors.HexColor('#87CEEB'),
            'AUG': colors.HexColor('#B0E0E6'),
            'SEP': colors.HexColor('#E0FFFF'),
            'OCT': colors.HexColor('#E6E6FA'),
            'NOV': colors.HexColor('#DDA0DD'),
            'DEC': colors.HexColor('#FFE4E1')
        }

        # Convert 0.5 cm to points (1 cm = 28.35 points)
        top_margin = 14.175  # 0.5 cm in points

        # Process each page
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            
            # Create a new PDF in memory
            packet = io.BytesIO()
            c = canvas.Canvas(packet, pagesize=(width, height))

            # Tab dimensions
            tab_width = 15
            usable_height = height - top_margin
            tab_height = usable_height / 12
            border_width = 1  # Width of the white border

            # First draw all colored rectangles
            for i, (month, color) in enumerate(month_colors.items()):
                y_position = height - top_margin - ((i + 1) * tab_height)
                
                # Draw colored rectangle
                c.setFillColor(color)
                c.rect(width - tab_width, y_position, tab_width, tab_height, fill=1, stroke=0)

            # Then draw white borders between tabs
            c.setStrokeColor(colors.white)
            c.setLineWidth(border_width)
            for i in range(1, 12):  # Draw lines between tabs
                y_position = height - top_margin - (i * tab_height)
                c.line(width - tab_width, y_position, width, y_position)

            # Finally add the text
            for i, (month, color) in enumerate(month_colors.items()):
                y_position = height - top_margin - ((i + 1) * tab_height)
                
                # Add month text vertically
                c.setFillColor(colors.black)
                c.setFont("Helvetica", 8)
                
                # Save the canvas state
                c.saveState()
                
                # Calculate center position for text
                text_x = width - (tab_width/2) - 4
                text_y = y_position + (tab_height/2)
                
                # Rotate and position the text
                c.translate(text_x, text_y)
                c.rotate(-90)
                
                # Draw the text centered
                c.drawCentredString(0, 0, month)
                
                # Restore the canvas state
                c.restoreState()

            c.save()
            packet.seek(0)

            # Create a new PDF with the tabs
            new_pdf = PdfReader(packet)
            watermark_page = new_pdf.pages[0]

            # Merge the original page with the tabs
            page.merge_page(watermark_page)
            writer.add_page(page)

        # Save the result
        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)
        return True

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting PDF modification...")
    success = add_tabs_to_pdf()
    if success:
        print("Successfully added tabs to the PDF!")
    else:
        print("Failed to modify the PDF. Please check if the input file is valid.")