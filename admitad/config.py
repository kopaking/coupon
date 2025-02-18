
import logging
import os
from dotenv import load_dotenv
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

load_dotenv()

# admitad
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
base64_header = os.getenv('BASE64_HEADER')
w_id = os.getenv('W_ID')

# banggood
affiliate_id = os.getenv('AFFILIATE_ID')

class AdmitadAPI:
    def __init__(self):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base64_header = base64_header
        self.w_id = w_id
        self.authenticate()
        self.headers = {'Authorization': 'Bearer ' + self.access_token}
        self.params = {'limit': 500}

    def authenticate(self):
        url = "https://api.admitad.com/token/"
        headers_access_token = {
            'Authorization': f'Basic {self.base64_header}',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
        data_access_token = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'advcampaigns advcampaigns_for_website banners coupons coupons_for_website short_link websites'
        }
        response_access_token = requests.post(url, headers=headers_access_token, data=data_access_token)
        refresh_token_response = response_access_token.json()
        refresh_token = refresh_token_response["refresh_token"]

        headers_refresh_token = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data_refresh_token = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': refresh_token,
        }

        response_refresh_token = requests.post(url, headers=headers_refresh_token, data=data_refresh_token)
        print(f'response_refresh_token - {response_refresh_token}')

        valor = response_refresh_token.json()
        print(f"access token = '{valor['access_token']}")
        self.access_token = valor['access_token']

    def get_coupons_data(self):
        headers = self.headers
        params = self.params
        url = f'https://api.admitad.com/coupons/website/{self.w_id}/'
        response = requests.get(url, headers=headers, params=params)
        print(f'response coupons {response}')
        response_json = response.json()
        return response_json

    def get_advcampaigns_data(self):
        headers = self.headers
        params = self.params
        url = f'https://api.admitad.com/advcampaigns/website/{self.w_id}/'
        response = requests.get(url, headers=headers, params=params)
        print(f'response advcampaigns {response}')
        response_json = response.json()
        return response_json
