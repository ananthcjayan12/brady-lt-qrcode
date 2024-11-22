import os
import boto3
import uuid  # Import the uuid module
from dotenv import load_dotenv

load_dotenv()

class S3Uploader:
    def __init__(self):
        self.aws_access_key_id = os.getenv("aws_access_key_id")
        self.aws_secret_access_key = os.getenv("aws_secret_access_key")
        print(self.aws_access_key_id)
        self.session = boto3.Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )

    def upload_to_s3(self, bucket_name,folder_name, file_path, org_name,ext,metadata=None):
        s3 = self.session.resource('s3')
        file_name = self._generate_file_name(org_name,ext)
        file_name = "public/"+folder_name+"/"+file_name
        s3.Bucket(bucket_name).upload_file(file_path, file_name, ExtraArgs=metadata)
        return file_name

    def _generate_file_name(self,org_name,ext):
        tail = org_name
        unique_id = str(uuid.uuid4())
     
        file_name = f"{tail}-{unique_id}.{ext}"
        print(file_name)
        return file_name
