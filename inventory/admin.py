from django.contrib import admin
from .models import Item

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'created_at')  # Ensure all fields exist in your model
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    ordering = ('-created_at',)  # Ensure created_at exists in the model

admin.site.register(Item, ItemAdmin)
