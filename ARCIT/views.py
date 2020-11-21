from django.contrib.auth import login, authenticate
<<<<<<< HEAD
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
=======
from django.shortcuts import render, redirect

from ARCIT.core.forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
>>>>>>> 8ef0257d2ad29b0b7d97beaf13e6a50cd46e3ddb
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
<<<<<<< HEAD
        form = UserCreationForm()
=======
        form = SignUpForm()
>>>>>>> 8ef0257d2ad29b0b7d97beaf13e6a50cd46e3ddb
    return render(request, 'signup.html', {'form': form})
