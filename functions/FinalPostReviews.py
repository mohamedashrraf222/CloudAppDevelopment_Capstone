import json
from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(args):
    
    
    api_key = "CdwObnLdugcpE7PNQGxwV-JTH3i7w7yyG6ifp77RGmE2"
    service_url = "https://894cec5b-94ad-47e3-a6a1-715fd7a8db9b-bluemix.cloudantnosqldb.appdomain.cloud"

    # Create an IAM Authenticator with the API key
    authenticator = IAMAuthenticator(api_key)

    # Create a Cloudant client instance
    cloudant_client = CloudantV1(authenticator=authenticator)
    cloudant_client.set_service_url(service_url)

    database_name = 'reviews'

    # Get the new document from the request body
    new_document = {k: v for k, v in args.items() if not k.startswith('__ow_')}
    


    if len(new_document) == 0:
        response = {
            'ok': False
        }
    else:
        # Insert the new document into the database 
        response = cloudant_client.post_document(db=database_name, document=new_document, headers= {'Content-Type': 'application/json'}).get_result()


    if response['ok'] :
        # Return the response
        return {
            'statusCode': 200,
            'body': 'Your document succeffully posted to the database'
        }
    else :
        return {
            'body': 'There was a problem ! Please give me valid data to post to the database.'
        }

if __name__ == '__main__':
    myresult = main({"dealership": 152})
    print(myresult)
