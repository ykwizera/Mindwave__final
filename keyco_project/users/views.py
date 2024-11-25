from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages

# Signup View
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return redirect('dashboard')
    return render(request, 'app/signup.html')

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'app/login.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# People View (list registered users)
def people_view(request):
    users = User.objects.all()
    return render(request, 'app/people.html', {'users': users})

# Dashboard View
def dashboard_view(request):
    return render(request, 'app/dashboard.html')
