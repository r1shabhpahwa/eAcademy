from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate


def homepage(request):
    return render(request, 'homepage.html')


def login_view(request):
    if request.method == 'POST':
        # Handle login form submission
        # Use the submitted data to authenticate the user
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # User is authenticated, log in the user
            login(request, user)
            return redirect('home')  # Replace 'home' with the URL name for your homepage
        else:
            # Authentication failed, show an error message
            error_message = 'Invalid username or password.'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        # Display the login form
        return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        # Handle register form submission
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Replace 'login' with the URL name for your login page
    else:
        # Display the register form
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

