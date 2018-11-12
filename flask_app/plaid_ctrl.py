""" This module does blah blah blah """

import plaid
from flask import json
from flask_app import errors, db

try:
    import keys
except IOError:
    print("Keys File not Found. Online Access")

PLAID_CLIENT = plaid.Client(keys.PLAID_API_KEYS['plaid_client_id'],
                            keys.PLAID_API_KEYS["plaid_secret"],
                            keys.PLAID_API_KEYS["plaid_public_key"],
                            keys.PLAID_API_KEYS["plaid_env"])

# PLAID_ACCESS_TOKEN = keys.PLAID_API_KEYS["plaid_access_token"]


def get_plaid_data(request):
    """
    description
    """
    try:
        balance_response = \
            None
#           PLAID_CLIENT.Accounts.balance.get(PLAID_ACCESS_TOKEN)
        balance = json.dumps(balance_response, indent=2, sort_keys=True)
        return balance

    except plaid.errors.PlaidError:
        raise errors.InvalidUsage('This view is gone', status_code=410)


def get_plaid_donations(request):
    """
    description
    """
