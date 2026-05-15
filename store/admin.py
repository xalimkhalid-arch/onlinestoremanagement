from django.contrib import admin
from .models import Product, Message

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'created_at']
    search_fields = ['name']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email','contact', 'created_at', 'is_read']
    search_fields = ['name', 'email']
    list_filter = ['is_read', 'created_at']
    fields = ['name', 'email', 'contact', 'message', 'reply', 'is_read']


# Register your models here.
