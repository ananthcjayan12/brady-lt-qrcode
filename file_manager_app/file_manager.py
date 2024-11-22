from .s3_uploader import S3Uploader
from .qr_code_generator import QRCodeGenerator
import os
from PIL import Image

class FileManager:
    def __init__(self, s3_uploader, qr_code_generator):
        self.s3_uploader = s3_uploader
        self.qr_code_generator = qr_code_generator

    def process_file(self, bucket_name, folder_name,file_path, org_name,url,metadata=None):
        ext="pdf"
        file_name = self.s3_uploader.upload_to_s3(bucket_name, folder_name,file_path,org_name, ext,metadata=metadata)
        s3_link = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
        qr_code_url = f"{url}?pdfFile={s3_link}"
        folder_name=folder_name+"qrcodes"
        qr_code_path = self.generate_qr_code(qr_code_url,bucket_name,org_name,folder_name)
        return qr_code_path

    def generate_qr_code(self, s3_link, bucket_name,file_name,folder_name):
        return self.qr_code_generator.generate_qr_code(s3_link, bucket_name,file_name,folder_name)

