import logging
import os
from pyrogram import Client
from dotenv import load_dotenv
import requests
import json
import asyncio

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

load_dotenv()

# telegram
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
allowed_user_id = os.getenv('ALLOWED_USER_ID')
channelid_global = os.getenv('CHANNELID_GLOBAL')
channelid_br = os.getenv('CHANNELID_BR')

# admitad
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
base64_header = os.getenv('BASE64_HEADER')
affiliate_id = os.getenv('AFFILIATE_ID')
w_id = os.getenv('W_ID')


class TelegramBot:
    def __init__(self):
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_token = bot_token
        self.allowed_user_id = allowed_user_id
        self.channelid_global = channelid_global
        self.channelid_br = channelid_br
        self.bot = None

    async def start_bot(self):
        self.bot = Client(
            "bot", api_id=int(api_id), api_hash=api_hash, bot_token=bot_token
            )
        await self.bot.start()

    async def send_message(self, chat_id, caption):
        if self.bot is None:
            await self.start_bot()
        await self.bot.send_message(chat_id=int(chat_id), text=caption)
        await asyncio.sleep(60)

    async def get_entity(self, user_id):
        if self.bot is None:
            await self.start_bot()
        return await self.bot.get_users(user_id)


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
        print(valor['access_token'])
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


class CouponPoster:
    def __init__(self):
        self.admitad_api = AdmitadAPI()
        self.telegram_bot = TelegramBot()
        self.posted_discounts = []

    async def post_global_admitad(self):
        coupons = self.admitad_api.get_coupons_data()
        advcampaigns = self.admitad_api.get_advcampaigns_data()
        
        discounts = coupons
        campaigns = advcampaigns
        
        posted_discounts = self.load_posted_discounts()

        for discount in discounts.get("results", []) + campaigns.get("results", []):
            if self.should_skip_discount(discount, posted_discounts):
                continue
            post_content = self.create_post_content(discount)
            posted_discounts.append(discount["id"])
            self.save_posted_discounts(posted_discounts)
            await self.telegram_bot.send_message(chat_id=int(channelid_global), caption=post_content)
            await self.send_confirmation_message()

                                   
    def load_posted_discounts(self):
        if not os.path.isfile('posted_discounts.json'):
            with open('posted_discounts.json', 'w') as f:
                json.dump([], f)

        with open('posted_discounts.json', 'r') as f:
            posted_discounts = json.load(f)
            return posted_discounts
        
    def save_posted_discounts(self, posted_discounts):
        with open('posted_discounts.json', 'w') as f:
            json.dump(posted_discounts, f)

    def should_skip_discount(self, discount, posted_discounts):
        return discount.get("id") in posted_discounts
        
    def create_post_content(self, discount):
        campaign_name = discount.get("campaign", {}).get("name", "").replace(" ", "_")
        post_content = f'🔥 #{campaign_name} 🔥\n\n'
        post_content += f'🛍️ {discount["name"]}\n'
        if "promocode" in discount and discount["promocode"] != 'NOT REQUIRED':
            post_content += f'Coupon:   `{discount["promocode"]}`\n'
        post_content += f'💰 Discount: {discount.get("discount", "")}\n' if discount.get("discount") is not None and '1%' not in discount.get("discount", "") else ''
        goto_link = discount.get("goto_link", "")
        if goto_link and 'https://aliaf.site/' not in goto_link:
            post_content += f'{self.shorten_url(goto_link)}\n\n'
        else:
            post_content += f'{goto_link}\n\n'
        return post_content

    async def send_confirmation_message(self):
        #user = await self.telegram_bot.get_entity(allowed_user_id)
        await self.telegram_bot.send_message(
            allowed_user_id,
            "The message was successfully posted on the GLOBAL channel!"
            )

    def shorten_url(self, url):
        headers = self.admitad_api.headers
        url_shortener_response = requests.post(
            'https://api.admitad.com/shortlink/modify/',
            headers=headers,
            json={'link': url}
        )
        #url_shortener_response.raise_for_status()
        url_shortener_data = url_shortener_response.json()
        return url_shortener_data['short_link']


async def main():
    coupon_poster = CouponPoster()
    await coupon_poster.post_global_admitad()

if __name__ == "__main__":
    asyncio.run(main())
