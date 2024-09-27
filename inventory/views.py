from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Item
from .serializers import ItemSerializer, UserSerializer
from django.shortcuts import get_object_or_404
import redis
import json  # To handle JSON serialization
from django.http import HttpResponse

# Initialize Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

class ItemView(APIView):
    def get(self, request, item_id=None):
        if item_id:
            # Try to get the item from Redis
            cached_item = redis_client.get(f'item:{item_id}')
            if cached_item:
                # Return the cached item (deserialized from JSON)
                return Response(json.loads(cached_item))

            # If not in Redis, get from DB
            item = get_object_or_404(Item, id=item_id)
            serializer = ItemSerializer(item)
            # Cache the serialized item data in Redis
            redis_client.set(f'item:{item_id}', json.dumps(serializer.data))  # Serialize data to JSON
            return Response(serializer.data)

        # Retrieve all items from the database
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Cache the new item in Redis
            redis_client.set(f'item:{serializer.data["id"]}', json.dumps(serializer.data))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Update the cache after modifying the item
            redis_client.set(f'item:{item_id}', json.dumps(serializer.data))  # Update cache
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        item.delete()
        # Remove the item from Redis cache after deletion
        redis_client.delete(f'item:{item_id}')
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# This should be a separate function, not inside the class
def home(request):
    return HttpResponse("Welcome to the Inventory Management System!")
