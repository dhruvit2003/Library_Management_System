from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .utils import write_data, read_data

class TestLibrary(APITestCase):
    def setUp(self):
        write_data([])
    
    def test_add_valid_book(self):
        url = reverse('add_book')

        #valid input
        valid_data = {
            'isbn': 1234567890123,
            'title': 'Automic Habits',
            'author': 'James Clear',
            'publication_year': 2018
        }
        response = self.client.post(url, valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 1)

    def test_add_book_with_invalid_ISNB_type(self):
        url = reverse('add_book')

        #invalid ISBN (not an integer)
        invalid_isbn_data = {
            'isbn': '1234567890123',
            'title': 'Automic Habits',
            'author': 'James Clear',
            'publication_year': 2018
        }
        response = self.client.post(url, invalid_isbn_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_book_with_invalid_length(self):
        url = reverse('add_book')
          
        #invalid ISBN (not 13 digits)
        invalid_isbn_length_data = {
            'isbn': 123456,
            'title': 'Automic Habits',
            'author': 'James Clear',
            'publication_year': 2018
        }
        response = self.client.post(url, invalid_isbn_length_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_book_with_invalid_year_type(self):
        url = reverse('add_book')
           
        #invalid publication year (not an integer)
        invalid_year_data = {
            'isbn': 9876543210123,
            'title': 'Automic Habits',
            'author': 'James Clear',
            'publication_year': '2018'
        }
        response = self.client.post(url, invalid_year_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_book_with_empty_title(self):
        url = reverse('add_book')
            
        # Empty title
        empty_title_data = {
            'isbn': 9876543210123,
            'title': '',
            'author': 'James Clear',
            'publication_year': 2018
        }
        response = self.client.post(url, empty_title_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_add_book_with_empty_author(self):
        url = reverse('add_book')
            
        # Empty author
        empty_author_data = {
            'isbn': 9876543210123,
            'title': 'Automic Habits',
            'author': '',
            'publication_year': 2018
        }
        response = self.client.post(url, empty_author_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

