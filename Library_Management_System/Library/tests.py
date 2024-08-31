from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .utils import write_data, read_data

class TestLibrary(APITestCase):
    def setUp(self):
        write_data([])
    
    #Add_book tests
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

    #Borrow_book tests
    def test_borrow_available_book(self):
        url = reverse('borrow_book', args=[1234567890123])
        data = [
            {
                'isbn': 1234567890123,
                'title': 'Automic Habits',
                'author': 'James Clear',
                'publication_year': 2018,
                'available': True
            }
        ]
        write_data(data)
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['available'])

    def test_borrow_unavailable_book(self):
        url = reverse('borrow_book', args=[1234567890123])
        data = [
            {
                'isbn': 1234567890123,
                'title': 'Automic Habits',
                'author': 'James Clear',
                'publication_year': 2018,
                'available': False #book is already borrowed
            }
        ]
        write_data(data)
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_borrow_nonexistent_book(self):
        url = reverse('borrow_book', args=[1234567890123])
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_borrow_invalid_ISNB_type(self):
        url = reverse('borrow_book', args=['1234567890123'])
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    #Return_book tests
    def test_return_borrowed_book(self):
        url = reverse('return_book', args=[1234567890123])
        data = [
            {
                'isbn': 1234567890123,
                'title': 'Automic Habits',
                'author': 'James Clear',
                'publication_year': 2018,
                'available': False  # Book is currently borrowed
            }
        ]
        write_data(data)
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['available'])

    def test_return_available_book(self):
        url = reverse('return_book', args=[1234567890123])
        data = [
            {
                'isbn': 1234567890123,
                'title': 'Automic Habits',
                'author': 'James Clear',
                'publication_year': 2018,
                'available': True  # Book is already available
            }
        ]
        write_data(data)
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_return_nonexistent_book(self):
        url = reverse('return_book', args=[1234567890123])
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_return_invalid_isbn(self):
        url = reverse('return_book', args=['invalid_isbn'])
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)