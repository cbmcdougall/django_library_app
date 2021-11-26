from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='library-index'),
    path('authors/<int:author_id>', views.show_author, name='author-show'),
    path('books/<int:book_id>/', views.show_book, name='book-show'),
    path('books/new/', views.create, name='book-create')
]
