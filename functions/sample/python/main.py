"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests
import os

couch_url = os.environ.get('COUCH_URL')
couch_username = os.environ.get('COUCH_USERNAME')
i_am_api_key = os.environ.get('IAM_API_KEY')


def main(param_dict):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """

    try:
        client = Cloudant.iam(
            account_name = couch_username or param_dict['COUCH_USERNAME'],
            api_key= i_am_api_key or param_dict['IAM_API_KEY'],
            connect=True,
        )
        print(f"Databases: {client.all_dbs()}")
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}
