from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .models import NewsItem, NewsSample, ContactResponse
from .forms import ContactForm, RegistrationForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.conf import settings

# Import Twilio for sending SMS
from twilio.rest import Client

# Twilio configuration
client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

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


def register(request):
    error_message = None
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            
            country_code = form.cleaned_data['country_code']
            half_phone_number = form.cleaned_data['phone_number']
            phone_number = f"{country_code}{half_phone_number}"
            
            # Check if a user with the provided phone number already exists
            if UserProfile.objects.filter(phone_number=phone_number).exists():
                messages.error(request, 'A user with this phone number already exists.')
            else:
                # Generate and send verification code (similar to previous examples)
                verification_code = generate_verification_code()
                send_verification_code(phone_number, verification_code)

                # Store the verification code in the session
                request.session['verification_code'] = verification_code

                # Store the form data in the session
                request.session['registration_data'] = form.cleaned_data

                return render(request, 'verify.html', {'phone_number': phone_number})

    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def verify(request):
    if request.method == 'POST':
        
        phone_number = request.POST.get('phone_number')
        code = request.POST.get('code')

        # Retrieve the stored verification code from the session
        stored_code = request.session.get('verification_code')

        if code == stored_code:
            # Code is valid, retrieve the registration data from the session
            registration_data = request.session.get('registration_data')
            country_code = registration_data['country_code']
            phone_number = registration_data['phone_number']
            full_phone_number = f"{country_code}{phone_number}"

            # Create and save the user
            User = get_user_model()  # Get the User model
            user = User.objects.create_user(
                phone_number=full_phone_number,
                password=registration_data['password'],
                first_name=registration_data['first_name'],
                last_name=registration_data['last_name'],
            )

            # Clear the session data
            del request.session['verification_code']
            del request.session['registration_data']
            messages.success(request, 'Account created successfully.')
            return redirect('login')  # Redirect to the login page
        else:
            messages.error(request, 'Invalid verification code. Please try again.')

    return render(request, 'verify.html')

def generate_verification_code():
    # Generate a 6-digit random verification code
    import random
    return str(random.randint(100000, 999999))

def send_verification_code(phone_number, code):
    # Send the verification code using Twilio
    message = client.messages.create(
        body=f'Your verification code is: {code}',
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    
def login_view(request):
    if request.method == 'POST':
        country_code = request.POST['country_code']
        half_phone_number = request.POST['phone_number']
        phone_number = f"{country_code}{half_phone_number}"
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
