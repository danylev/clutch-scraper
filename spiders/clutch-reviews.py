import json

import scrapy
from scrapy import Selector
from scrapy.http import HtmlResponse

from scrapy_splash import SplashRequest

with open('ladder.json') as fd:
    companies = json.load(fd)
    companies = companies[:85]

class ClutchListSpider(scrapy.Spider):
    name = "clutch-profile"
    companies = companies
    company = companies.pop()
    start_urls = [f'https://clutch.co/widgets/get/21371/5']
    data = None

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, dont_filter=True, args={'wait': 1.0})

    def parse(self, response):
        if self.company['reviews']:
            if self.data is None:
                self.data = self.company
                self.data['feedback'] = []
            for review in response.css('div.review-border > div.clearfix'):
                reviewer = review.css('h2 > span::text').extract_first()
                type_of, budget, date, *_= review.css('div.hidden-xs.abs-aligned').css('div.field-items > div.field-item::text').extract() + [None, None, None]
                rating = review.css('div.description > span.field-label.number::text').extract_first()
                quality, schedule, cost, refer, *_ = review.css('div.group-fdb-feedback > div.field > div.field-items > div.field-item > div.clearfix::text').extract() + [None, None, None, None]
                sphere, size, area, verified, *_ = review.css('div.group-fdb-interview > div.field > div.field-items > div.field-item::text').extract() + [None, None, None, None]
                review_data = {
                    'case': reviewer,
                    'kind': type_of,
                    'budget': budget,
                    'date': date,
                    'rating': rating,
                    'quality': quality,
                    'schedule': schedule,
                    'cost': cost,
                    'refering': refer,
                    'sphere': sphere,
                    'size': size.split()[0] if size else None,
                    'area': area,
                    'verified': bool(verified), 
                }
                self.data['feedback'].append(review_data)
            while response.css('li.pager-next a::attr(href)').extract_first():
                yield response.follow(f"https://clutch.co{response.css('li.pager-next a::attr(href)').extract_first()}", self.parse)
            yield self.data
            self.data = None
        # self.company = companies.pop()
        # yield SplashRequest(f'https://clutch.co/widgets/get/{(self.company["nid"])}/5', self.parse, dont_filter=True, args={'wait': 0.5})
