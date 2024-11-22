import os
import qrcode
import uuid
from fpdf import FPDF

class QRCodeGenerator:
    def __init__(self):
        self._create_qr_code_folder()

    def _create_qr_code_folder(self):
        folder_path = "media/finalqrcodes"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

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

        # Generate a unique file name
        unique_filename = str(uuid.uuid4()) + '.png'
        qr_code_path = os.path.join("media/finalqrcodes", unique_filename)

        # Save the QR Code image
        qr_image.save(qr_code_path)

        return qr_code_path
    
    def generate_qr_code_as_pdf(self, url):
        qr_code_path = self.generate_qr_code(url)
        
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
        pdf.image(qr_code_path, x=qr_x, y=qr_y, w=qr_code_size, h=qr_code_size)

        # Generate a unique PDF filename
        unique_pdf_filename = str(uuid.uuid4()) + '.pdf'
        pdf_path = os.path.join("media/finalpdfs", unique_pdf_filename)

        pdf.output(pdf_path)

        return pdf_path
