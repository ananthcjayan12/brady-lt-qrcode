import qrcode
import uuid
from fpdf import FPDF
import io
from PIL import Image
import base64
import tempfile
import os

class QRCodeGenerator:
    def __init__(self):
        pass

    def generate_qr_code(self, url):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Save QR code to bytes buffer instead of file
        img_buffer = io.BytesIO()
        qr_image.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        return img_buffer
    
    def generate_qr_code_as_pdf(self, url):
        qr_buffer = self.generate_qr_code(url)
        
        # Create a temporary file to store the image
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
            tmp_file.write(qr_buffer.getvalue())
            tmp_file_path = tmp_file.name
        
        try:
            pdf = FPDF('P', 'mm', (100, 60))
            pdf.add_page()
            pdf.set_auto_page_break(auto=False)

            # Set font for text
            pdf.set_font("Arial", size=12)

            # QR Code Area
            pdf.set_fill_color(255)  # Set fill color to white
            qr_code_size = 30
            
            # Position the QR code 1 cm from the right edge
            qr_x = 100 - qr_code_size - 1  # 10mm or 1 cm gap from the right
            # Vertically center the QR code
            qr_y = (60 - qr_code_size) / 2
            pdf.rect(qr_x, qr_y, qr_code_size, qr_code_size, 'F')  # F is for fill
            
            # Use the temporary file path
            pdf.image(tmp_file_path, x=qr_x, y=qr_y, w=qr_code_size, h=qr_code_size)

            # Get PDF as bytes
            pdf_bytes = pdf.output(dest='S').encode('latin1')  # Get PDF as bytes
            
            # Convert to base64 for easy embedding in HTML
            pdf_base64 = base64.b64encode(pdf_bytes).decode()
            return f"data:application/pdf;base64,{pdf_base64}"
            
        finally:
            # Clean up the temporary file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
