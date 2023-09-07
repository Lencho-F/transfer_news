from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .models import NewsItem, NewsSample, ContactResponse
from .forms import ContactForm
from django.contrib import messages

##def home(request):
    ##  news_samples = NewsSample.objects.all()
   ## return render(request, 'home.html', {'news_samples': news_samples})
# views.py
from django.http import JsonResponse


def home(request):
    news_samples = NewsSample.objects.all()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save() 
    else:
        form = ContactForm()
        news_samples = NewsSample.objects.all()

    return render(request, 'home.html', {'form': form, 'news_samples': news_samples})



def login_view(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        user = authenticate(request, phone_number=phone_number, password=password)
        if user is not None:
            login(request, user)
            return redirect('secret_page')
        else:
            messages.error(request, 'Invalid phone number or password')
            return redirect('login')  # Redirect back to the login page with an error message
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to the desired page after logout (e.g., the home page)

@login_required
def secret_page(request):
    news_items = NewsItem.objects.all()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save() 
    else:
        form = ContactForm()
        news_items = NewsItem.objects.all()
        
    return render(request, 'secret_page.html', {'form': form, 'news_items': news_items})
