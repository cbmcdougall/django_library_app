from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import UserSignupForm

# Create your views here.
def register(req):
    if req.user.is_authenticated:
        return redirect('library-index')
    if req.method == "POST":
        form = UserSignupForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req, user)
            username = form.cleaned_data.get('username')
            messages.success(req, f"Registration successful, {username}")
            return redirect('library-index')
    else:
        form = UserSignupForm()
    data = { "form": form }
    return render(req, "users/signup.html", data)