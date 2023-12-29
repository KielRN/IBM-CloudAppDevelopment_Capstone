import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

#Create a 'get_request' to make HTTP GET requests
def get_request(url, **kwargs):
    
    api_key = kwargs.get("api_key")

    try:
        # Call get method of requests library with api_key
        if api_key:
            response = requests.get(url, params=params,headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
        # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
        status_code = response.status_code
        json_data = json.load(response.text)
        return json_data
    except:
        print("Something went wrong")
        return None

# Create a get_dealers_from_cf method to get dealers from a cloud function
# - Call get_request() with specified arguments (State)
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    state = kwargs.get("state")
    # Call get_request with a URL parameter
    if state:
        json_result = get_request(url, state=state)
    else:    
        json_result = get_request(url)

    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
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
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_reviews_from_cf(url, dealer_id, **kwargs):
    results = []
    json_result = get_request(url, id=dealer_id)

    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result
        # remove duplicates in reviews
        nodup_reviews =[i for n, i in enumerate(reviews) if i not in reviews[:n]]
        # For each dealer object
        for review in nodup_reviews:
            # Get its content in `doc` object
            review_doc = review
            sentiment=analyze_review_sentiments(review_doc["review"])
            # Create a DealerReview object with values in `doc` object
            if "purchase_date" in review_doc:
                purchase_date = review_doc['purchase_date']
            else:
                purchase_date = "00/00/000"
            if "car_make" in review_doc:
                car_make = review_doc['car_make']
            else:
                car_make = "None"
            if "car_model" in review_doc:
                car_model = review_doc['car_model']
            else:
                car_model = "None"
            if "car_year" in review_doc:
                car_year = review_doc['car_year']
            else:
                car_year = 0000
            
            dealerReview_obj = DealerReview(dealership=review_doc["dealership"], name=review_doc["name"], purchase=review_doc["purchase"],
                                review=review_doc["review"], purchase_date=purchase_date, car_make=car_make,
                                car_model=car_model,
                                car_year=car_year, sentiment = sentiment,id=review_doc['id'])
            results.append(dealerReview_obj)
            
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerreview):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/734f74a7-ef14-4103-a664-54574f909e3f"
    api_key = "EhYbgYCw6iGWm-laTvbwTH0Y_brDqNavDCJz6NuxzKil"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01', authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    
    response = natural_language_understanding.analyze(
        text=dealerreview,
        features=Features(sentiment=SentimentOptions(targets=[dealerreview])),
        language="en"
    ).get_result()
    
    
    label = response['sentiment']['document']['label']

    return label
