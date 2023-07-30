from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import requests
import json

def main(param_dict):
    api_key = "CdwObnLdugcpE7PNQGxwV-JTH3i7w7yyG6ifp77RGmE2"
    service_url = "https://894cec5b-94ad-47e3-a6a1-715fd7a8db9b-bluemix.cloudantnosqldb.appdomain.cloud"

    # Create an IAM Authenticator with the API key
    authenticator = IAMAuthenticator(api_key)

    # Create a Cloudant client instance
    cloudant_client = CloudantV1(authenticator=authenticator)
    cloudant_client.set_service_url(service_url)

    if 'dealership' in param_dict:
        myselector = {
            'dealership': {'$eq': param_dict['dealership']}
        }

        response = cloudant_client.post_find(
            db='reviews',
            selector=myselector,
        ).get_result()
        # Extract the documents and return them
        documents = response['docs']
    else:
        response = cloudant_client.post_all_docs(
            db='reviews',
            include_docs=True
        ).get_result()
        # Extract the documents and return them
        documents = response['rows']


    # Return the JSON response
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': documents
    }


if __name__ == '__main__':
    myresult = main({'dealership':15})
    print(myresult)
