import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from dotenv import load_dotenv

# Load environment variables using python-dotenv
load_dotenv()
env_value = os.getenv("environment")

# Check environment variable and set the appropriate Django settings module
if env_value == "local":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FileUploadQRCodeGenerator.settings")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FileUploadQRCodeGenerator.settings_prod")

# Get the default Django WSGI application
application = get_wsgi_application()

# Use WhiteNoise to serve static files
# Replace 'FileUploadQRCodeGenerator' with the name of your Django project if different
from FileUploadQRCodeGenerator import settings
application = WhiteNoise(application, root=settings.STATIC_ROOT)



