from django.shortcuts import render
from .file_manager import S3Uploader, QRCodeGenerator, FileManager
import os
from PIL import Image
from .models import Folder, WhatsAppMessage, OutgoingWhatsAppMessage, WhatsappLogs
from django.urls import reverse
import tempfile
from django.shortcuts import render
from .file_manager import QRCodeGenerator  # Make sure to import your QRCodeGenerator
import uuid
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
import requests
import json
from django.conf import settings
from dotenv import load_dotenv
from .whatsapp_config import WHATSAPP_CONFIG

load_dotenv()


@login_required
def index(request):
    pdf_data = None

    if request.method == "POST":
        url = request.POST.get("url")

        if url:
            qr_code_generator = QRCodeGenerator()
            pdf_data = qr_code_generator.generate_qr_code_as_pdf(url)

    return render(request, "index.html", {"pdf_data": pdf_data})


# Other functions can remain the same


def view_pdf(request):
    return render(request, "pdf_view.html")


def display_qr_code(qr_code_path):
    if qr_code_path:
        image = Image.open(qr_code_path)
        image.thumbnail((300, 300))
        return image

    return None


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.urls import reverse


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("qrcodeurl:index"))
        else:
            # Return an 'invalid login' error message.
            return render(request, "login.html", {"error": "Invalid login credentials"})

    return render(request, "login.html")


from django.contrib.auth import logout
from django.shortcuts import redirect


def user_logout(request):
    logout(request)
    url = reverse("qrcodeurl:login")
    return redirect(reverse("qrcodeurl:login"))


def send_whatsapp_message(to_number, menu_message):
    headers = {
        "Authorization": f"Bearer {WHATSAPP_CONFIG['API_TOKEN']}",
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": menu_message},
    }
    response = requests.post(WHATSAPP_CONFIG['API_URL'], headers=headers, json=data)
    return response.json()


def send_interactive_message(phone_number, message):
    headers = {
        "Authorization": f"Bearer {WHATSAPP_CONFIG['API_TOKEN']}",
        "Content-Type": "application/json",
    }
    # Constructing the payload for the interactive message
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": message["body"]},
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": button["reply"]["id"],
                            "title": button["reply"]["title"],
                        },
                    }
                    for button in message["buttons"]
                ]
            },
            "header": {"type": "text", "text": message["header"]},
            "footer": {"text": message["footer"]},
        },
    }

    # Sending the HTTP request
    response = requests.post(WHATSAPP_CONFIG['API_URL'], headers=headers, data=json.dumps(payload))
    WhatsappLogs.objects.create(
        sent_to_number=phone_number, message_text="hi", response_data=response.json()
    )
    # Return the API response
    return response.json()



def extract_sender_number(payload):
    try:
        sender_number = payload["entry"][0]["changes"][0]["value"]["contacts"][0][
            "wa_id"
        ]
    except (KeyError, IndexError):
        sender_number = "Unknown"
    return sender_number


def extract_message_text(payload):
    try:
        message_text = payload["entry"][0]["changes"][0]["value"]["messages"][0][
            "text"
        ]["body"].lower()
    except (KeyError, IndexError):
        message_text = ""
    return message_text


class WhatsAppWebhookView(APIView):
    def get(self, request, *args, **kwargs):
        hub_mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if hub_mode == "subscribe" and token == WHATSAPP_CONFIG['VERIFY_TOKEN']:
            return HttpResponse(challenge)
        return HttpResponse("Verification failed", status=403)

    # def post(self, request, *args, **kwargs):
    #     incoming_payload = request.data
    #     sender_number = incoming_payload.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('contacts', [])[0].get('wa_id', 'Unknown')
    #     message_details = incoming_payload.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('messages', [])[0]
    #     message_text = message_details.get('text', {}).get('body', '')
    #     message_id = message_details.get('id', '')
    #     timestamp = message_details.get('timestamp', '')

    #     # Store in database
    #     WhatsAppMessage.objects.create(
    #         sender_number=sender_number,
    #         message_text=message_text,
    #         message_id=message_id,
    #         timestamp=timestamp,
    #         payload=incoming_payload,
    #     )

    #     # Check if the message text contains "menu"
    #     if "menu" in incoming_payload.get('message', {}).get('text', '').lower():  # Adjust based on actual payload structure
    #         # Prepare your response message
    #         response_message = {
    #             "messages": [
    #                 {"text": "Our menu items: chicken porotta lime"}
    #             ]
    #         }
    #         return Response(response_message, status=status.HTTP_200_OK)

    #     # For other messages, you might want to return a different response or no response
    #     return Response({"message": "No menu request detected"}, status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        incoming_payload = request.data
        sender_number = extract_sender_number(incoming_payload)
        message_text = extract_message_text(incoming_payload)

        # Save the incoming message
        if sender_number != "Unknown":
            WhatsAppMessage.objects.create(
                sender_number=sender_number,
                message_text=message_text,
                payload=incoming_payload,
            )

        # Determine response based on incoming message
        # if "hi" in message_text:
        #     response_message = "Welcome to our service! How can we assist you today?"
        if "hi" in message_text.lower():
            # Construct a message with buttons using the WhatsApp Business API format
            header = "Hi! Welcome to Dubai Hut Dine engage service."
            body = "Please select an option:"
            footer = "Powered by Dubai Hut"
            buttons = [
                {"type": "reply", "reply": {"id": "order_menu", "title": "Order"}},
                {
                    "type": "reply",
                    "reply": {
                        "id": "visit_social_media",
                        "title": "Visit Social Media",
                    },
                },
            ]
            response_message = {
                "header": header,
                "body": body,
                "footer": footer,
                "buttons": buttons,
            }
            # Send response via WhatsApp API with buttons
            api_response = send_interactive_message(sender_number, response_message)
        elif "menu" in message_text:
            response_message = "Here's our menu: [Menu Details Here]"  # Adjust with actual menu details
        elif "order submitted" in message_text.lower():
            # Generate order summary and create a response with buttons
            order_summary = """Order Summary 📄:

Items Ordered:
- Chicken Biryani x3
- Falooda x1

Total Amount: 420 Dirhams 💰

What would you like to do next?"""
            header = "Order Submitted Successfully"
            body = order_summary
            footer = "What would you like to do next?"
            buttons = [
                {
                    "type": "reply",
                    "reply": {"id": "order_again", "title": "Order Again"},
                },
                {
                    "type": "reply",
                    "reply": {"id": "generate_bill", "title": "Generate Bill"},
                },
                # Add a third button if needed, for example:
                {
                    "type": "reply",
                    "reply": {"id": "contact_support", "title": "Contact Support"},
                },
            ]
            response_message = {
                "header": header,
                "body": body,
                "footer": footer,
                "buttons": buttons,
            }
            # Send interactive message response
            api_response = send_interactive_message(sender_number, response_message)
        # elif "generate bill" in message_text.lower():
        #     # Assume pdf_url is the URL of the PDF bill you want to send
        #     pdf_url = "https://www.clickdimensions.com/links/TestPDFfile.pdf"  # Replace with actual PDF URL
        #     # Call send_pdf_bill function to send the PDF document
        #     api_response = send_pdf_bill(sender_number, pdf_url)
        else:
            response_message = "How can I help you? For menu, type 'menu'."

        # Send response via WhatsApp API and store the outgoing message and API response
        api_response = send_whatsapp_message(sender_number, response_message)
        if sender_number != "Unknown":
            OutgoingWhatsAppMessage.objects.create(
                sent_to_number=sender_number,
                message_text=response_message,
                response_data=api_response,
            )

        return Response({"message": "Response sent"}, status=status.HTTP_200_OK)
