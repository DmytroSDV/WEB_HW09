import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'quote': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
        
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

class AuthorSpider(scrapy.Spider):
    name = 'authors'
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        author_links = response.css('div.quote a::attr(href)').getall()
        for link in author_links:
            yield response.follow(link, self.parse_author)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        yield {
            'fullname': response.css('h3.author-title::text').get(),
            'born_date': response.css('span.author-born-date::text').get(),
            'born_location': response.css('span.author-born-location::text').get(),
            'description': response.css('div.author-description::text').get().strip(),
        }