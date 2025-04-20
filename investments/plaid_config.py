# investments/plaid_config.py

from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.link_token_account_filters import LinkTokenAccountFilters
from plaid.model.depository_filter import DepositoryFilter
from plaid.model.account_subtype import AccountSubtype
from plaid.model.account_type import AccountType
from dotenv import load_dotenv
from plaid import Configuration, ApiClient
import os


configuration = Configuration(
    host="https://sandbox.plaid.com",  # This is fine for sandbox testing
    api_key={
        'clientId': os.getenv("PLAID_CLIENT_ID"),
        'secret': os.getenv("PLAID_SECRET"),
    }
)

api_client = ApiClient(configuration)
plaid_client = plaid_api.PlaidApi(api_client)
