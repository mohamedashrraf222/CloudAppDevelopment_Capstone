from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from .restapis import get_dealers_from_cf
from .restapis import get_dealer_reviews_from_cf
from .restapis import post_request

# Get an instance of a logger
logger = logging.getLogger(__name__)


# this view is for rendering static template file
# it takes the user from the request and pass it to the html page within the context
def render_static(request):
    context = {}
    return render(request, 'djangoapp/static_template.html', context)


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(
                username=username, password=password)
            login(request, user)
            print(user)
            return redirect("djangoapp:static_template")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:static_template')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'static_template.html', context)
    else:
        return render(request, 'static_template.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:static_template')


# Update the `get_dealerships` view to render the index page with a list of dealerships
# this view is for "dealers/"
def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/9ab8b676-a577-447e-9cf0-95c442855153/dealership-package/get-dealership"
        
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)

        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        context = {
            'dealership_list':dealerships
            }
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, **kwargs):

    url = "https://us-south.functions.appdomain.cloud/api/v1/web/9ab8b676-a577-447e-9cf0-95c442855153/dealership-package/get-review"
    dealership_details = get_dealer_reviews_from_cf(
        url=url, dealerId=kwargs['dealer_id'])
    context = {
        'reviews':dealership_details,
        'dealer_id':kwargs['dealer_id']
    }

    return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
@csrf_exempt
def add_review(request, **kwargs):
    # in the kwargs there is the dealer_id
    if request.method == "POST":
        required_fields = [
            'name',
            'purchase',
            'review',
            'purchase_date',
            'car_make',
            'car_model',
            'car_year',
            'id'
        ]
        missing_fields = [field for field in required_fields if request.POST.get(field) is None]
        if missing_fields:
            print('the missing fields',missing_fields)
            response_data = {
                'error': True,
                'message': f"You have to post all data. Missing fields: {', '.join(missing_fields)}"
            }
            return JsonResponse(response_data, status=400)
        
        theRevi = {
            'dealership': int(kwargs.get('dealer_id')),
            'name': request.POST.get('name'),
            'purchase': request.POST.get('purchase'),
            'review': request.POST.get('review'),
            'purchase_date': request.POST.get('purchase_date'),
            'car_make': request.POST.get('car_make'),
            'car_model': request.POST.get('car_model'),
            'car_year': request.POST.get('car_year'),
            'id': request.POST.get('id'),
        }
        print(theRevi)
        url = 'https://us-south.functions.appdomain.cloud/api/v1/web/9ab8b676-a577-447e-9cf0-95c442855153/dealership-package/post-review'
        myres = post_request(url=url, params=theRevi)
        # return HttpResponse(myres)
        return redirect("djangoapp:dealer_details", dealer_id=kwargs.get('dealer_id'))
    elif request.method == "GET":
        context = {'dealer_id':kwargs.get('dealer_id')}
        return render(request, 'djangoapp/add_review.html', context)
