import aiohttp
from bs4 import BeautifulSoup


async def get_profile_img_url(profile_url: str, session: aiohttp.ClientSession) -> str | None:
    base_url = 'https://www.abgeordnetenwatch.de'
    timeout = aiohttp.ClientTimeout(total=10)
    async with session.get(profile_url, timeout=timeout) as r:
        if not r.ok:
            return None
        img_src = parse_profile_img(await r.text())
        return f"{base_url}{img_src}" if img_src else None

def parse_profile_img(content: str) -> str | None:
    soup = BeautifulSoup(content, 'html.parser')
    img = soup.select_one(
        'figure.profile-header__picture__figure img[src]'
    )
    return img['src'] if img else None
