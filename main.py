import asyncio
from dotenv import load_dotenv

from admitad.handlers import CouponPoster


async def main():
    coupon_poster = CouponPoster()
    await coupon_poster.post_global_admitad()

if __name__ == "__main__":
    asyncio.run(main())