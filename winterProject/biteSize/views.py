from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Index page
def index(request):
    return render(request, "biteSize/index.html")

# Login page
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if not username:
            return render(request, "biteSize/login.html", {
                "error": "Enter a Username"
            })
        
        if not User.objects.filter(username=username).exists():
            return render(request, "biteSize/login.html", {
                "error": "Username does not exist"
            })

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect("index")
        else:
            # Invalid credentials
            return render(request, "biteSize/login.html", {
                "error": "Invalid credentials"
            })

        
    return render(request, "biteSize/login.html")

# Register page
def register(request):
    if request.method == "POST":
        username = request.POST["username"].strip()
        password = request.POST["password"]
        confirmPassword = request.POST["confirmPassword"]

        if not username:
            return render(request, "biteSize/register.html", {
                "error": "Enter a Username"
            })
        
        if not password or not confirmPassword:
            return render(request, "biteSize/register.html", {
                "error": "Enter a Username"
            })


        # Check if the username already exits
        if User.objects.filter(username=username).exists():
            return render(request, "biteSize/register.html", {
                "error": "Username already exists"
            })

        if password != confirmPassword:
            return render(request, "biteSize/register.html", {
                "error": "Passwords do not match"
            })

        # Check for strong password
        if len(password) < 8:
            return render(request, "biteSize/register.html", {
                "error": "Passwords must be at least 8 characters long"
            })

        user = User.objects.create_user(username=username, password=password)
        user.save()
        auth_login(request, user)

        return redirect("index")

    return render(request, "biteSize/register.html")