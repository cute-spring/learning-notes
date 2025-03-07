import sys
import io
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color

def is_read_only(annot_obj):
    """
    Determine if a widget field is marked as read-only.
    Checks the annotation's /Ff flag. If not found, it looks in the parent field.
    Returns True if the read-only flag (bit 1) is set.
    """
    ff = annot_obj.get('/Ff')
    if ff is None:
        parent = annot_obj.get('/Parent')
        if parent:
            parent_obj = parent.get_object()
            ff = parent_obj.get('/Ff', 0)
        else:
            ff = 0
    return bool(int(ff) & 1)

def get_field_type(annot_obj):
    """
    Retrieve the field type (/FT) from the annotation object or its parent.
    Common values: /Tx (text), /Btn (button), /Ch (choice).
    Returns None if not found.
    """
    field_type = annot_obj.get('/FT')
    if field_type is None:
        parent = annot_obj.get('/Parent')
        if parent:
            parent_obj = parent.get_object()
            field_type = parent_obj.get('/FT')
    return field_type

def get_field_name(annot_obj):
    """
    Retrieve the field name (/T) from the annotation object or its parent.
    Returns None if not found.
    """
    field_name = annot_obj.get('/T')
    if field_name is None:
        parent = annot_obj.get('/Parent')
        if parent:
            parent_obj = parent.get_object()
            field_name = parent_obj.get('/T')
    return field_name

def create_overlay(reader):
    """
    Create an overlay PDF that:
      1) Highlights only fillable fields (not read-only, and /FT in ['/Tx', '/Btn', '/Ch']).
      2) Displays the index number of each field on that page.
      3) Logs field details (name, index, page, field type, bounding box, read-only status) to console.
    """
    packet = io.BytesIO()
    can = canvas.Canvas(packet)
    num_pages = len(reader.pages)
    
    for page_num in range(num_pages):
        page = reader.pages[page_num]
        # Determine page dimensions from the mediabox
        mediabox = page.mediabox
        width = float(mediabox.upper_right[0]) - float(mediabox.lower_left[0])
        height = float(mediabox.upper_right[1]) - float(mediabox.lower_left[1])
        can.setPageSize((width, height))
        
        field_counter = 0  # Will increment for each editable widget on this page
        
        if '/Annots' in page:
            annots = page['/Annots']
            for annot in annots:
                annot_obj = annot.get_object()
                
                # Only process widget annotations
                if annot_obj.get('/Subtype') == '/Widget':
                    # Check if it's a recognized field type
                    field_type = get_field_type(annot_obj)
                    if field_type not in ['/Tx', '/Btn', '/Ch']:
                        continue
                    
                    # Skip if the widget is read-only
                    if is_read_only(annot_obj):
                        continue
                    
                    rect = annot_obj.get('/Rect')
                    if rect:
                        # This is an editable field, so increment our index
                        field_counter += 1
                        
                        # Retrieve bounding box
                        llx, lly, urx, ury = [float(coord) for coord in rect]
                        rect_width = urx - llx
                        rect_height = ury - lly
                        
                        # Draw a semi-transparent highlight (e.g., green)
                        can.setFillColor(Color(0, 1, 0, alpha=0.3))
                        can.rect(llx, lly, rect_width, rect_height, fill=1, stroke=0)
                        
                        # Display the index number inside the highlight
                        can.setFillColor(Color(0, 0, 0, alpha=1))
                        can.setFont("Helvetica", 8)
                        center_x = llx + rect_width / 2
                        center_y = lly + rect_height / 2
                        can.drawCentredString(center_x, center_y, str(field_counter))
                        
                        # Log the field details to the console
                        field_name = get_field_name(annot_obj)
                        print(
                            f"[Page {page_num+1}, Field {field_counter}] "
                            f"Name: {field_name}, Type: {field_type}, "
                            f"BBox: ({llx}, {lly}, {urx}, {ury}), "
                            f"ReadOnly: {is_read_only(annot_obj)}"
                        )
                        
        can.showPage()
    can.save()
    packet.seek(0)
    return packet

def main(input_pdf, output_pdf):
    reader = PdfReader(input_pdf)
    overlay_stream = create_overlay(reader)
    overlay_pdf = PdfReader(overlay_stream)
    writer = PdfWriter()

    for page_num, page in enumerate(reader.pages):
        overlay_page = overlay_pdf.pages[page_num]
        page.merge_page(overlay_page)
        writer.add_page(page)

    with open(output_pdf, 'wb') as f_out:
        writer.write(f_out)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python highlight_pdf_fields.py input.pdf output.pdf")
    else:
        main(sys.argv[1], sys.argv[2])