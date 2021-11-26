from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import reverse

from .models import Author, Book

# Create your tests here.
class BaseTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = Author.objects.create(name="Jimmy Bob")
        cls.book = Book.objects.create(title="Bobbing Along", author=cls.author)
        cls.user = User.objects.create_user("Pingu", "pingu@nootnoot.com", "nootnoot")

class TestBasicViews(BaseTestCase):
    c = Client()

    def test_index(self):
        response = self.c.get(reverse('library-index'))
        assert "books" in response.context
        assert "authors" in response.context
        assert response.context['books'].count() == 1
        assert "library/index.html" in [t.name for t in response.templates]

    def test_show_author(self):
        response = self.c.get("author-show")
        assert "library/404.html" in [t.name for t in response.templates]
    
    def test_show_book(self):
        response = self.c.get("book-show")
        assert "library/404.html" in [t.name for t in response.templates]

    def test_create(self):
        response = self.c.get("book-create")
        assert "library/404.html" in [t.name for t in response.templates]

class TestLoggedInViews(BaseTestCase):

    def setUp(self):
        self.c = Client()
        self.c.login(username="Pingu", password="nootnoot")

    def test_show_author_load(self):
        response = self.c.get(reverse("author-show", kwargs={"author_id": self.author.id}))
        assert "authors/show.html" in [t.name for t in response.templates]
    
    def test_show_book_load(self):
        response = self.c.get(reverse("book-show", kwargs={"book_id": self.book.id}))
        assert "books/show.html" in [t.name for t in response.templates]

    def test_show_book_404(self):
        books = Book.objects.all()
        response = self.c.get(reverse("book-show", kwargs={"book_id": len(books) + 1}))
        assert "library/404.html" in [t.name for t in response.templates]
        self.assertContains(response, "Sorry, we couldn't find that book!")
    
    def test_show_author_404(self):
        authors = Author.objects.all()
        response = self.c.get(reverse("author-show", kwargs={"author_id": len(authors) + 1}))
        assert "library/404.html" in [t.name for t in response.templates]
        self.assertContains(response, "Sorry, we couldn't find that author!")

    def test_create_page_load(self):
        response = self.c.get(reverse("book-create"))
        assert "books/new.html" in [t.name for t in response.templates]
        self.assertContains(response, "title")
        self.assertContains(response, "author")
        self.assertContains(response, "new_author")

    def test_create_new_book(self):
        data = {
            "title": "Bobbing Along 2: Jimmy Boogaloo",
            "author": self.author.id
        }
        response = self.c.post(reverse("book-create"), data=data)
        assert Book.objects.filter(title=data["title"]).exists()
        self.assertRedirects(response, reverse("book-show", kwargs={"book_id": 2}))

    def test_create_new_book_no_authors(self):
        data = {
            "title": "I have no author"
        }
        response = self.c.post(reverse("book-create"), data=data)
        self.assertContains(response, "Must specify an Author!")

    def test_create_existing_book(self):
        existing_book = self.book.title
        existing_author = Author.objects.filter(name=self.book.author).values_list("id", flat=True).first()
        data = {
            "title": existing_book,
            "author": existing_author
        }
        response = self.c.post(reverse("book-create"), data=data)
        self.assertContains(response, "That book is already in our system!")

    def test_create_new_author(self):
        data = {
            "title": "The Nootrients of Life: 50 Recipes for Fish",
            "new_author": "Pingu"
        }
        response = self.c.post(reverse("book-create"), data=data)
        assert Book.objects.filter(title=data["title"]).exists()
        assert Author.objects.filter(name=data["new_author"]).exists()

    def test_borrow_book(self):
        data = {
            "borrower": self.user.id
        }
        # Check book is available
        response = self.c.get(reverse("book-show", kwargs={ "book_id": self.book.id}))
        self.assertContains(response, "Available")
        # Check can borrow book
        response = self.c.post(reverse("book-show", kwargs={ "book_id": self.book.id}), data=data)
        response = self.c.get(reverse("book-show", kwargs={ "book_id": self.book.id}))
        self.assertContains(response, "On Loan")
        # Check can return book
        response = self.c.post(reverse("book-show", kwargs={ "book_id": self.book.id}), data=data)
        response = self.c.get(reverse("book-show", kwargs={ "book_id": self.book.id}))
        self.assertContains(response, "Available")

