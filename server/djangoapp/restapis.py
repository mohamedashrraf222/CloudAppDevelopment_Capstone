import requests
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import SentimentOptions, Features
# import related models here
from .models import CarDealer
from .models import DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):

    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url,params,**kwargs):
    print(params)
    try:
        response = requests.get(url=url, params=params)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        return response # Parse the response as JSON
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # For each dealer object
        for dealer in json_result:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter that returns list with all reviews
    json_result = get_request(
        url=url, dealer=kwargs['dealerId'] if isinstance(kwargs['dealerId'], int) else 15)

    if json_result:
        # For each view object
        for review in json_result:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = DealerReview(name=review['name'], dealership=review['dealership'], purchase=review['purchase'],
                                      review=review['review'], car_model=review['car_model'], car_year=review['car_year'], sentiment=analyze_review_sentiments(review['review']), id=review['id'], purchase_date=review['purchase_date'], car_make=review['car_make'])
            results.append(dealer_obj)
    # returns a list with objects of dealer's reviews
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerreview):
    api_key = 'g2nasPeBYSwXUzM7iEmwpm12_pbjkqAYsWe21BWBWmq2'
    service_url = 'https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/f94c8975-af87-4626-8e11-59010acec5b8'

    authenticator = IAMAuthenticator(api_key)
    
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-08-01',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(service_url)
    try:
        response = natural_language_understanding.analyze(
            text=dealerreview,
            features=Features(sentiment=SentimentOptions())
        ).get_result()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    # Extract the sentiment score from the response
    sentiment_score = response['sentiment']['document']['score']

    # Determine the sentiment label based on the score
    if sentiment_score >= 0.75:
        sentiment_label = 'Very Positive'
    elif sentiment_score >= 0.45:
        sentiment_label = 'Positive'
    elif sentiment_score >= -0.2:
        sentiment_label = 'Neutral'
    elif sentiment_score >= -0.75:
        sentiment_label = 'Negative'
    else:
        sentiment_label = 'Very Negative'

    return sentiment_label



