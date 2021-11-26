from django import forms
from .models import Book, Author

class NewBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']

     # only need to define `new_author`, other fields come automatically from model
    new_author = forms.CharField(max_length=30, required=False, label = "Author name (if not in list)")

    def __init__(self, *args, **kwargs):
        super(NewBookForm, self).__init__(*args, **kwargs)
        # make `author` not required, we'll check for one of `author` or `new_author` in the `clean` method
        self.fields['author'].required = False

    def clean(self):
        author = self.cleaned_data.get('author')
        new_author = self.cleaned_data.get('new_author')
        if not author and not new_author:
            # neither was specified so raise an error to user
            raise forms.ValidationError('Must specify an Author!')
        elif not author:
            # get/create `Author` from `new_author` and use it for `author` field
            author, created = Author.objects.get_or_create(name=new_author)
            self.cleaned_data['author'] = author

        # Check if book already exists
        author = self.cleaned_data.get('author')    # Get updated author
        title = self.cleaned_data.get('title')
        if Book.objects.filter(title=title, author=author):
            raise forms.ValidationError('That book is already in our system!')

        return super(NewBookForm, self).clean()

class BorrowBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['borrower']
        widgets = {'borrower': forms.HiddenInput()}