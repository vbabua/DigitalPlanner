from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import *
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

def add_clickable_tabs(input_pdf="output_with_copies.pdf", output_pdf="output_with_clickable_tabs.pdf"):
    try:
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        # Get the dimensions from the first page
        first_page = reader.pages[0]
        width = float(first_page.mediabox.width)
        height = float(first_page.mediabox.height)

        # Define tab dimensions
        top_margin = 14.175  # 0.5 cm in points
        tab_width = 25
        usable_height = height - top_margin
        tab_height = usable_height / 12

        # Define months and their corresponding page numbers (0-based index)
        month_links = {
            'JAN': 1,  # Links to page 2
            'FEB': 2,  # Links to page 3
            'MAR': 3,
            'APR': 4,
            'MAY': 5,
            'JUN': 6,
            'JUL': 7,
            'AUG': 8,
            'SEP': 9,
            'OCT': 10,
            'NOV': 11,
            'DEC': 12
        }

        # Process each page
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            writer.add_page(page)
            
            annotations = []
            # Create annotation for each month tab
            for i, (month, target_page) in enumerate(month_links.items()):
                y_position = height - top_margin - ((i + 1) * tab_height)
                
                # Create rectangle annotation (clickable area)
                rect = RectangleObject([
                    FloatObject(width - tab_width),
                    FloatObject(y_position),
                    FloatObject(width),
                    FloatObject(y_position + tab_height)
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
        
        print(f"Successfully created PDF with clickable tabs: {output_pdf}")
        return True

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    print("Adding clickable tabs to PDF...")
    success = add_clickable_tabs()
    if not success:
        print("Failed to modify the PDF. Please check if the input file is valid.")