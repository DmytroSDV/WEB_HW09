import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json

from customs.custom_timer import async_time

class QuotePageScrapping:
    def __init__(self, main_url):
        self.main_url = main_url

    async def get_page_text(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()
                return BeautifulSoup(text, 'html.parser')

    async def get_quotes(self, content):
        result_list = []
        quotes = content.find_all('div', class_='quote')

        for quote in quotes:
            temp_dict = {}
            temp_dict['quote'] = quote.find("span", class_='text').get_text()
            temp_dict['author'] = quote.find("small", class_='author').get_text()
            temp_dict['tags'] = quote.find('div', class_='tags').find('meta', class_='keywords').get('content').split(",")
            result_list.append(temp_dict)

        return result_list

    async def get_authors(self, content):
        result_list = []
        author_links = content.find_all('a', href=lambda value: value and "/author/" in value)
    
        for link in author_links:
            temp_dict = {}
            page_text = await self.get_page_text(self.main_url + link.get("href"))
            autors = page_text.find_all('div', class_="author-details")
            for author in autors:
                temp_dict['fullname'] = author.find("h3", class_="author-title").get_text()
                temp_dict['born_date'] = author.find("span", class_="author-born-date").get_text()
                temp_dict['born_location'] = author.find("span", class_="author-born-location").get_text()
                temp_dict['description'] = author.find("div", class_="author-description").get_text().strip()
                result_list.append(temp_dict)

        return result_list

    def save_to_json(self, data, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

@async_time
async def main():        
    quotes = []
    authors = []

    main_url = 'http://quotes.toscrape.com'
    scrappy = QuotePageScrapping(main_url)
    page_text = await scrappy.get_page_text(main_url)

    while True:
        quotes.extend(await scrappy.get_quotes(page_text))
        authors.extend(await scrappy.get_authors(page_text))

        next_page_link = page_text.find('li', class_='next')
        if next_page_link is None:
            break

        next_page_url = main_url + next_page_link.find('a')['href']
        page_text = await scrappy.get_page_text(next_page_url)

    scrappy.save_to_json(quotes, 'quotes.json')
    scrappy.save_to_json(authors, 'authors.json')

if __name__ == '__main__':
    asyncio.run(main())
