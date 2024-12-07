from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import Image
from .models import Profile

# Public Views
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')

# Authentication Views
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if the user has a profile
            try:
                _ = user.profile
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('home')
            except Profile.DoesNotExist:
                messages.error(request, "Invalid credentials. Please try again.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('home')

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user and trigger the Profile signal
            messages.success(request, "Signup successful! Please log in.")
            return redirect('login')  # Redirect to login page
        else:
            messages.error(request, "Signup failed. Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def forgot_password(request):
    return render(request, 'forgot_password.html')

@login_required
def my_works(request):
    images = Image.objects.filter(user=request.user)  # Assuming Image model has a `user` field
    return render(request, 'my_works.html', {'images': images})


@login_required
def upload_image(request):
    if request.method == "POST":
        title = request.POST['title']
        image = request.FILES['image']
        description = request.POST['description']
        
        # Save the new image with the user
        Image.objects.create(title=title, image=image, description=description, user=request.user)
        messages.success(request, "Image uploaded successfully!")
        return redirect('my_works')
    return render(request, 'upload_image.html')


@login_required
def delete_image(request, image_id):
    try:
        image = Image.objects.get(id=image_id)
        image.delete()
        messages.success(request, "Image deleted successfully!")
    except Image.DoesNotExist:
        messages.error(request, "Image not found.")
    return redirect('my_works')

@login_required
def update_image(request, image_id):
    try:
        image = Image.objects.get(id=image_id)
        if request.method == "POST":
            title = request.POST['title']
            description = request.POST['description']
            if 'image' in request.FILES:
                image.image = request.FILES['image']
            image.title = title
            image.description = description
            image.save()
            messages.success(request, "Image updated successfully!")
            return redirect('my_works')
    except Image.DoesNotExist:
        messages.error(request, "Image not found.")
    return render(request, 'update_image.html', {'image': image})
