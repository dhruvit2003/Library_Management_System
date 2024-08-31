from django.urls import path
from . import views

urlpatterns = [
    path('add_book/', views.AddBook.as_view(), name='add_book'),
    path('borrow_book/<str:pk>/', views.BorrowBook.as_view(), name='borrow_book'),
    path('return_book/<str:pk>/', views.ReturnBook.as_view(), name='return_book'),
    path('available_books/', views.ViewAvailableBooks.as_view(), name='available_books'),
]