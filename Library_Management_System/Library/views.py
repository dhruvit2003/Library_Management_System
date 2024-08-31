from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import write_data, read_data
from datetime import datetime as date

class AddBook(APIView):
    def post(self, request):
        data = read_data()

        #validation
        isbn = request.data['isbn']
        title = request.data['title']
        author = request.data['author']
        publication_year = request.data['publication_year']

        #validation to check ISNB is an integer and 13 digits
        if not isinstance(isbn, int) or len(str(isbn)) != 13:
            return Response({'error': 'ISBN must be a 13-digit integer'}, status=status.HTTP_400_BAD_REQUEST)

        #validation to check the isbn is unique
        if any(book['isbn'] == isbn for book in data):
            return Response({'error': 'ISBN already exists'}, status=status.HTTP_400_BAD_REQUEST)

        #validation to check the title and author are not empty
        if not title or not author:
            return Response({'error': 'Title and author are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        #validation to check the publication year is an integer and in the past
        if not isinstance(publication_year, int) or publication_year > date.today().year:
            return Response({'error': 'Publication year must be an integer in the past'}, status=status.HTTP_400_BAD_REQUEST)

        #adding new book
        new_book = {
            'isbn': isbn,
            'title': title,
            'author': author,
            'publication_year': publication_year, 
            'available': True
        }
        data.append(new_book)
        write_data(data)
        return Response(data, status=status.HTTP_201_CREATED)

class BorrowBook(APIView):
    def patch(self, request, pk):
        data = read_data()

        #validation to check the ISBN is an integer
        try:
            isbn = int(pk)
        except ValueError:
            return Response({"error": "ISBN must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        book = next((book for book in data if book['isbn'] == isbn), None)

        if book is None:
            return Response({"error": "Book not found."}, status=status.HTTP_400_BAD_REQUEST)

        if not book['available']:
            return Response({"error": "Book is currently unavailable."}, status=status.HTTP_400_BAD_REQUEST)

        book['available'] = False 
        write_data(data)
        return Response(book, status=status.HTTP_200_OK)

class ReturnBook(APIView):
    def patch(self, request, pk):
        data = read_data()

        try:
            isbn = int(pk)
        except ValueError:
            return Response({"error": "ISBN must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        book = next((book for book in data if book['isbn'] == isbn), None)

        if book is None:
            return Response({"error": "Book not found."}, status=status.HTTP_400_BAD_REQUEST)

        if book['available']:
            return Response({"error": "Book is already available."}, status=status.HTTP_400_BAD_REQUEST)

        book['available'] = True
        write_data(data)
        return Response(book, status=status.HTTP_200_OK)
    
class ViewAvailableBooks(APIView):
    def get(self, request):
        data = read_data()
        
        available_books = [book for book in data if book['available']]
        
        return Response(available_books, status=status.HTTP_200_OK)