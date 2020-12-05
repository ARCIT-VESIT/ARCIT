from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from ARCIT.core.forms import MyModelForm, SignUpForm
from ARCIT.models import MyModel


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


class CreateMyModelView(CreateView):
    model = MyModel
    form_class = MyModelForm
    template_name = 'template.html'


