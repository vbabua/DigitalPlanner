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
            tab_width = 40
            usable_height = height - top_margin
            tab_height = usable_height / 12  # Divide the remaining height by number of months

            # Add tabs
            for i, (month, color) in enumerate(month_colors.items()):
                # Calculate position for current tab
                y_position = height - top_margin - ((i + 1) * tab_height)
                
                # Draw tab rectangle
                c.setFillColor(color)
                c.rect(width - tab_width, y_position, tab_width, tab_height, fill=1)

                # Add month text
                c.setFillColor(colors.black)
                c.setFont("Helvetica", 8)
                # Center the text in the tab
                text_y = y_position + (tab_height/2) - 4  # Adjust the 4 points for better centering
                c.drawString(width - tab_width + 5, text_y, month)

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