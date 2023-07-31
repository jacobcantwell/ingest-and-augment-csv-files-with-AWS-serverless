# api reqests can take more than 3 seconds so update the Configuration -> General configuration -> Timeout

import requests # imported via a lambda layer - https://api.klayers.cloud/api/v2/p3.10/layers/latest/ap-southeast-2/html OR build your own
import json
import uuid # used in mocking api response
import random # used in mocking api response
import time # used in mocking longer response

# api-endpoint - should be an environmental variable or passed in via Systems Manager Parameter 
URL = "https://catfact.ninja/facts?limit=100"

def lambda_handler(event, context):

    # python requests API - https://requests.readthedocs.io/en/latest/
    api_response = requests.get(URL)
    print(f"r.status_code: {api_response.status_code}")
    json_response = api_response.json()
    # get key in API JSON
    cat_facts = json_response['data']
    print(f"cat_facts: {cat_facts}")
    cat_fact = cat_facts[random.randint(1, 10)]['fact']
    print(f"cat_fact: {cat_fact}")
    
    # create a random UUID
    subscription_uuid = uuid.uuid4().hex
    
    # mock function taking longer to respond - make sure Lambda configuration timeout is longer than 3s default
    print("Starting... \n")
    time.sleep(2) # Sleeping for one second
    print("Back to the future..")
    
    return {
        'body': { 
            'SubscriptionUuid': subscription_uuid,
            'SubscriptionName': 'hey_taxi',
            'Fact': cat_fact
        }
    }

