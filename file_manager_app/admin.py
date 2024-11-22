from django.contrib import admin
from .models import WhatsAppMessage,OutgoingWhatsAppMessage,WhatsappLogs

@admin.register(WhatsAppMessage)
class WhatsAppMessageAdmin(admin.ModelAdmin):
    list_display = ('received_at', 'sender_number', 'message_text', 'message_id', 'timestamp','payload')
    search_fields = ('sender_number', 'message_text')

@admin.register(OutgoingWhatsAppMessage)
class OutgoingWhatsAppMessageAdmin(admin.ModelAdmin):
    list_display = ['sent_to_number', 'message_text', 'sent_at']
    search_fields = ['sent_to_number', 'message_text']
    readonly_fields = ['response_data', 'sent_at']

@admin.register(WhatsappLogs)
class WhatsappLogsAdmin(admin.ModelAdmin):
    list_display = ['sent_to_number', 'message_text', 'sent_at']
    search_fields = ['sent_to_number', 'message_text']
    readonly_fields = ['response_data', 'sent_at']