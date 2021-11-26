from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .forms import BorrowBookForm, NewBookForm
from .models import Author, Book

# Library Methods
def index(req):
    books = Book.objects.all().order_by('author', 'title')
    authors = Author.objects.all().order_by('name')
    data = { "books": books, "authors": authors }
    return render(req, 'library/index.html', data)

@login_required
def show_author(req, author_id):
    try:
        author = get_object_or_404(Author, pk=author_id)
        author_books = Book.objects.filter(author=author).order_by("title")
        data = { "author": author.name, "books": author_books }
        return render(req, 'authors/show.html', data)
    except Http404:
        data = { "no_author": True }
        return render(req, 'library/404.html', data)

@login_required
def show_book(req, book_id):
    try:
        book = get_object_or_404(Book, pk=book_id)
        author = Author.objects.filter(name=book.author).first()
        if req.method == "POST":
            form = BorrowBookForm(req.POST)
            if form.is_valid():
                if book.borrower == req.user:
                    book.borrower = None
                else:
                    book.borrower = req.user
                book.save()
                return redirect("book-show", book_id=book_id)
        else:
            form = BorrowBookForm(initial={"borrower": req.user})
        data = { "book": book, "author": author, "form": form }
        return render(req, 'books/show.html', data)
    except Http404:
        data = { "no_book": True }
        return render(req, 'library/404.html', data)

@login_required
def create(req):
    if req.method == "POST":
        form = NewBookForm(req.POST)
        if form.is_valid():
            book_id = form.save().id
            return redirect("book-show", book_id=book_id)
    else:
        form = NewBookForm()
    data = {"form": form}
    return render(req, "books/new.html", data)
    

# Error Handling Methods
def not_found_404(req, exception):
    data = { "err": exception }
    return render(req, 'library/404.html', data)

def server_error_500(req):
    return render(req, 'library/500.html')