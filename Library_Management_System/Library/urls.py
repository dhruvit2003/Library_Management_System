from django.urls import path
from . import views

urlpatterns = [
    path('add_book/', views.AddBook.as_view(), name='add_book'),
]