import os
from dotenv import load_dotenv

load_dotenv()

WHATSAPP_CONFIG = {
    'API_URL': "https://graph.facebook.com/v18.0/243259928866558/messages",
    'API_TOKEN': os.getenv('WHATSAPP_API_TOKEN'),
    'VERIFY_TOKEN': os.getenv('WHATSAPP_VERIFY_TOKEN')
} 