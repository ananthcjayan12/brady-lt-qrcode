import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from dotenv import load_dotenv



# Check environment variable and set the appropriate Django settings module

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FileUploadQRCodeGenerator.settings")


# Get the default Django WSGI application
application = get_wsgi_application()

# Use WhiteNoise to serve static files
# Replace 'FileUploadQRCodeGenerator' with the name of your Django project if different
from FileUploadQRCodeGenerator import settings
application = WhiteNoise(application, root=settings.STATIC_ROOT)



