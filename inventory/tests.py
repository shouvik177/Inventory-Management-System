from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Item

class ItemAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item_data = {'name': 'Test Item', 'description': 'Test Description'}

    def test_create_item(self):
        response = self.client.post('/api/items/', self.item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_items(self):
        Item.objects.create(**self.item_data)  # Create an item to test retrieval
        response = self.client.get('/api/items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure one item is returned

    def test_read_item(self):
        item = Item.objects.create(**self.item_data)  # Create an item
        response = self.client.get(f'/api/items/{item.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], item.name)  # Check item name

    def test_update_item(self):
        item = Item.objects.create(**self.item_data)  # Create an item
        response = self.client.put(f'/api/items/{item.id}/', {'name': 'Updated Item'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item.refresh_from_db()  # Refresh the item instance from the database
        self.assertEqual(item.name, 'Updated Item')  # Check if the name was updated

    def test_delete_item(self):
        item = Item.objects.create(**self.item_data)  # Create an item
        response = self.client.delete(f'/api/items/{item.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Check if the item was deleted
        self.assertFalse(Item.objects.filter(id=item.id).exists())
