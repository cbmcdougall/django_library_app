# Django Library App

A library website built using django, to learn django!

## About the library

Users can:

- Access a homepage which lists all the books and authors stored in a library
- Register an account with the library to login with
- Log in so they can:
  - View individual pages for books/authors
    - Authors' pages shows a list of books by that author in the library
  - View a book's availability, and borrow it from the library if available
  - Return a book to the library to make it available for others
  - Add a new book to the library
    - Users must specify a book title and author

## Installation & Usage

### Installation

- Clone or download this repo
- `cd` into the repo folder
- Run `pipenv install` to install dependencies (_or install with your manager of choice from the provided requirements.txt_)

### Usage

- Run `pipenv shell` to enter the virtual environment
- `cd` into `library-app/` within the environment
- Run `python manage.py runserver` to start the django app
  - The site is then viewable on port 8000
- Run `python manage.py test` to run the test suites
- Run `pipenv run coverage && pipenv run coverage_report` to generate a test coverage report & view it
