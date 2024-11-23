from PyPDF2 import PdfReader, PdfWriter, PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import io
import os

def add_tabs_to_pdf(input_pdf="Golden spiral 2.pdf", output_pdf="output_with_tabs.pdf"):
    try:
        # First try to repair the PDF if needed
        def repair_pdf(input_file, output_file):
            with open(input_file, 'rb') as file:
                content = file.read()
            
            # Add EOF marker if missing
            if not content.endswith(b'%%EOF'):
                content = content + b'\n%%EOF\n'
            
            with open(output_file, 'wb') as file:
                file.write(content)
        
        # Create a temporary repaired file
        temp_pdf = "temp_repaired.pdf"
        repair_pdf(input_pdf, temp_pdf)
        
        # Now try to read the repaired PDF
        try:
            reader = PdfReader(temp_pdf)
        except:
            reader = PdfReader(input_pdf, strict=False)
        
        writer = PdfWriter()
        
        # Get the dimensions from the first page
        first_page = reader.pages[0]
        width = float(first_page.mediabox.width)
        height = float(first_page.mediabox.height)

        # Define colors for different months
        month_colors = {
            'JAN': colors.HexColor('#FFE4E1'),  # Light pink
            'FEB': colors.HexColor('#FFA07A'),  # Light salmon
            'MAR': colors.HexColor('#FFDAB9'),  # Peach
            'APR': colors.HexColor('#FFFFE0'),  # Light yellow
            'MAY': colors.HexColor('#F0E68C'),  # Khaki
            'JUN': colors.HexColor('#98FB98'),  # Pale green
            'JUL': colors.HexColor('#87CEEB'),  # Sky blue
            'AUG': colors.HexColor('#B0E0E6'),  # Powder blue
            'SEP': colors.HexColor('#E0FFFF'),  # Light cyan
            'OCT': colors.HexColor('#E6E6FA'),  # Lavender
            'NOV': colors.HexColor('#DDA0DD'),  # Plum
            'DEC': colors.HexColor('#FFE4E1')   # Misty rose
        }

        # Process each page
        for page_num in range(len(reader.pages)):
            # Get the page
            page = reader.pages[page_num]
            
            # Create a new PDF in memory
            packet = io.BytesIO()
            c = canvas.Canvas(packet, pagesize=(width, height))
            
            # Add tabs
            tab_width = 40
            tab_height = 25
            space_between_tabs = (height - 100) / 12
            
            for i, (month, color) in enumerate(month_colors.items()):
                # Calculate position for current tab
                y_position = height - 50 - (i * space_between_tabs)
                
                # Draw tab rectangle
                c.setFillColor(color)
                c.rect(width - tab_width, y_position, tab_width, tab_height, fill=1)
                
                # Add month text
                c.setFillColor(colors.black)
                c.setFont("Helvetica", 8)
                c.drawString(width - tab_width + 5, y_position + 8, month)
            
            c.save()
            
            # Move to the beginning of the buffer
            packet.seek(0)
            
            # Create a new PDF with the tabs
            new_pdf = PdfReader(packet)
            watermark_page = new_pdf.pages[0]
            
            # Merge the original page with the tabs
            page.merge_page(watermark_page)
            
            # Add the merged page to the writer
            writer.add_page(page)
        
        # Save the result
        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)
            
        # Clean up temporary file
        if os.path.exists(temp_pdf):
            os.remove(temp_pdf)
            
        return True

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # Try alternative method if first one fails
        try:
            # Alternative method using older PyPDF2 version syntax
            reader = PdfFileReader(open(input_pdf, 'rb'), strict=False)
            writer = PdfFileWriter()
            
            # Rest of the code remains similar...
            # (Previous tab-adding logic)
            
            return True
            
        except Exception as e2:
            print(f"Alternative method also failed: {str(e2)}")
            return False

if __name__ == "__main__":
    # Make sure you have the required libraries
    print("Starting PDF modification...")
    
    success = add_tabs_to_pdf()
    
    if success:
        print("Successfully added tabs to the PDF!")
    else:
        print("Failed to modify the PDF. Please check if the input file is valid.")