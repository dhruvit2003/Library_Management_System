from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .utils import write_data, read_data

# Create your tests here.
class TestLibrary(APITestCase):
    def setUp(self):
        write_data([])
    
    def test_add_book(self):
        url = reverse('add_book')
        data = {'isbn': '3010', 'title': 'Atomic Habit', 'author': 'James Clear', 'publication_year': '2018'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(read_data()), 5)
