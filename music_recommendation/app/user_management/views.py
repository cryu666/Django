import csv
import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

from .models import Users


def registerPage(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]  # add email input in html
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            # Check if the username already exists in the Users model
            if Users.objects.filter(username=username).exists():
                messages.error(request, 'Username "%s" is already in use.' % username)
                return render(request, "register.html", {"form": form})

            # Write the new user's account information to the Users model
            user = Users(username=username, password=password, email=email)
            user.save()
            print('User "%s" created' % username)
            messages.success(request, "Registration successed. Please login.")
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})


def loginPage(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = Users.objects.get(username=username, password=password)
        if user is not None:
            request.session["user_id"] = user.user_id
            messages.success(request, "Login successed.")
            return redirect("home")

        messages.error(request, "Invalid username or password.")
        return redirect("login")

    return render(request, "login.html")


def logout_view(request):
    if "user_id" in request.session:
        del request.session["user_id"]
        messages.success(request, "Logout successed.")
    return redirect("home")
