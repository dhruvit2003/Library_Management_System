from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .utils import write_data, read_data

class TestLibrary(APITestCase):
    def setUp(self):
        write_data([])
    
    def add_book(self, book_data):
        url = reverse('add_book')
        return self.client.post(url, book_data, format='json')

    def borrow_book(self, isbn):
        url = reverse('borrow_book', args=[isbn])
        return self.client.patch(url, format='json')

    def return_book(self, isbn):
        url = reverse('return_book', args=[isbn])
        return self.client.patch(url, format='json')

    def view_available_books(self):
        url = reverse('available_books')
        return self.client.get(url, format='json')

    #Add_book tests
    def test_add_valid_book(self):
        #valid input
        valid_data = {
            'isbn': 1234567890123,
            'title': 'Automic Habits',
            'author': 'James Clear',
            'publication_year': 2018
        }
        response = self.add_book(valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 1)

    def test_add_book_with_invalid_ISNB_type(self):
        #invalid ISBN (not an integer)
        invalid_isbn_data = {
            'isbn': '1234567890123',
            'title': 'Automic Habits',
            'author': 'James Clear',
            'publication_year': 2018
        }
        response = self.add_book(invalid_isbn_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_book_with_invalid_length(self):
        #invalid ISBN (not 13 digits)
        invalid_isbn_length_data = {
            'isbn': 123456,
            'title': 'Automic Habits',
            'author': 'James Clear',
            'publication_year': 2018
        }
        response = self.add_book(invalid_isbn_length_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_book_with_invalid_year_type(self):
        #invalid publication year (not an integer)
        invalid_year_data = {
            'isbn': 9876543210123,
            'title': 'Automic Habits',
            'author': 'James Clear',
            'publication_year': '2018'
        }
        response = self.add_book(invalid_year_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_book_with_empty_title(self):
        # Empty title
        empty_title_data = {
            'isbn': 9876543210123,
            'title': '',
            'author': 'James Clear',
            'publication_year': 2018
        }
        response = self.add_book(empty_title_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_add_book_with_empty_author(self):          
        # Empty author
        empty_author_data = {
            'isbn': 9876543210123,
            'title': 'Automic Habits',
            'author': '',
            'publication_year': 2018
        }
        response = self.add_book(empty_author_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #Borrow_book tests
    def test_borrow_available_book(self):
        isbn = 1234567890123
        data = [
            {
                'isbn': isbn,
                'title': 'Automic Habits',
                'author': 'James Clear',
                'publication_year': 2018,
                'available': True #book is available
            }
        ]
        write_data(data)
        response = self.borrow_book(isbn)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['available'])

    def test_borrow_unavailable_book(self):
        isbn = 1234567890123
        data = [
            {
                'isbn': isbn,
                'title': 'Automic Habits',
                'author': 'James Clear',
                'publication_year': 2018,
                'available': False #book is already borrowed
            }
        ]
        write_data(data)
        response = self.borrow_book(isbn)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_borrow_nonexistent_book(self):
        isbn = 1234567890123
        response = self.borrow_book(isbn)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_borrow_invalid_ISNB_type(self):
        isbn = "1234567890123"
        response = self.borrow_book(isbn)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    #Return_book tests
    def test_return_borrowed_book(self):
        isbn = 1234567890123
        data = [
            {
                'isbn': isbn,
                'title': 'Automic Habits',
                'author': 'James Clear',
                'publication_year': 2018,
                'available': False  # Book is currently borrowed
            }
        ]
        write_data(data)
        response = self.return_book(isbn)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['available'])

    def test_return_available_book(self):
        isbn = 1234567890123
        data = [
            {
                'isbn': isbn,
                'title': 'Automic Habits',
                'author': 'James Clear',
                'publication_year': 2018,
                'available': True  # Book is already available
            }
        ]
        write_data(data)
        response = self.return_book(isbn)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_return_nonexistent_book(self):
        isbn = 1234567890123
        response = self.return_book(isbn)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_return_invalid_isbn(self):
        isbn = "1234567890123"
        response = self.return_book(isbn)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    #view_books tests
    def test_view_available_books(self):
        data = [
            {
                 'isbn': 1234567890123,
                'title': 'Automic Habits',
                'author': 'James Clear',
                'publication_year': 2018,
                'available': True
            },
            {
                'isbn': 9876543210123,
                'title': 'Pride and Prejudice',
                'author': 'Jane Austen',
                'publication_year': 1813,
                'available': False
            }
        ]
        write_data(data)
        response = self.view_available_books()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['isbn'], 1234567890123)

    def test_view_no_available_books(self):
        data = [
            {
                'isbn': 1234567890123,
                'title': 'Automic Habits',
                'author': 'James Clear',
                'publication_year': 2018,
                'available': False
            },
            {
                'isbn': 9876543210123,
                'title': 'Pride and Prejudice',
                'author': 'Jane Austen',
                'publication_year': 1813,
                'available': False
            }
        ]
        write_data(data)
        response = self.view_available_books()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  

    def test_view_books_in_empty_library(self):
        response = self.view_available_books()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0) 