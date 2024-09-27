from django.urls import path
from .views import ItemView, home

urlpatterns = [
    path('', home, name='home'),  # Home view for root URL
    path('items/', ItemView.as_view(), name='items-list'),  # To list all items or create a new one
    path('items/<int:item_id>/', ItemView.as_view(), name='item-detail'),  # To get, update or delete a specific item
]