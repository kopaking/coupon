import logging
import os
import requests
import json
from dotenv import load_dotenv

from admitad.config import AdmitadAPI
from bot import TelegramBot

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



class CouponPoster:
    def __init__(self):
        self.admitad_api = AdmitadAPI()
        self.telegram_bot = TelegramBot()
        self.channelid_global = channelid_global
        self.channelid_br = channelid_br
        self.allowed_user_id = allowed_user_id
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
        if not os.path.isfile('data/posted_discounts.json'):
            with open('data/posted_discounts.json', 'w') as f:
                json.dump([], f)

        with open('data/posted_discounts.json', 'r') as f:
            posted_discounts = json.load(f)
            return posted_discounts
        
    def save_posted_discounts(self, posted_discounts):
        with open('data/posted_discounts.json', 'w') as f:
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
            int(allowed_user_id),
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
