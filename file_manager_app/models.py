from django.db import models

# Create your models here.
class Folder(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    


class WhatsAppMessage(models.Model):
    received_at = models.DateTimeField(auto_now_add=True)
    sender_number = models.CharField(max_length=20)
    message_text = models.TextField(blank=True, null=True)
    payload = models.JSONField()
    message_id = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f"Message from {self.sender_number} at {self.received_at}: {self.message_text}"

class OutgoingWhatsAppMessage(models.Model):
    sent_to_number = models.CharField(max_length=20)
    message_text = models.TextField()
    response_data = models.JSONField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message to {self.sent_to_number} at {self.sent_at}"
    
class WhatsappLogs(models.Model):
    sent_to_number = models.CharField(max_length=20,default="")
    message_text = models.TextField(null=True,blank=True)
    response_data = models.JSONField(null=True,blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message to {self.sent_to_number} at {self.sent_at}"
