from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarModel, DealerReview
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Views by ElliottRN


def static_view(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/static.html', context)


# Create an `about` view to render a static about page
# def about(request):
def about_view(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)




# Create a `contact` view to return a static contact page
#def contact(request):
def contact_view(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)



# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                messages.info(request, f"You are now logged in as {username}")
                return redirect('index')  # Replace 'index' with the name of the view you want to redirect to
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'djangoapp/login.html', {'form': form})


# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")  # Optional: Display a success message
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)



# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    url ='https://eliudlamboy-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get'
    dealerships = get_dealers_from_cf(url)
    context['dealership_list'] = dealerships
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request, dealer_id):
    if(request.method == "GET"):
        context = {}
        dealer_url = "https://eliudlamboy-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        reviews_url = "https://eliudlamboy-5000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews"
        dealerships = get_dealers_from_cf(dealer_url, id =dealer_id)
        context['dealership'] = dealerships[0]
        dealership_reviews = get_dealer_reviews_from_cf(reviews_url, id=dealer_id)
        context['review_list'] = dealership_reviews
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

