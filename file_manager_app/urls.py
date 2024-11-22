from django.urls import path
from . import views

app_name = 'qrcodeurl'
urlpatterns = [
    path('', views.index, name='index'),
    path('viewpdf/', views.view_pdf, name='viewpdf'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('webhook/whatsapp/', views.WhatsAppWebhookView.as_view(), name='whatsapp_webhook')
]
