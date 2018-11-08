import json

import scrapy
from scrapy import Selector

from scrapy_splash import SplashRequest

with open('ladder.json') as fd:
    companies = json.load(fd)
    companies = companies

class ClutchListSpider(scrapy.Spider):
    name = "clutch-profile"

    company = companies.pop()
    start_urls = [f'https://clutch.co{(company["url"])}']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, dont_filter=True, args={'wait': 1.0})

    def parse(self, response):
        data_dict = self.company
        charts_data = {}
        charts = response.css('div.chart-wrapper')
        for chart in charts:
            chart_data = {}
            chart_name = chart.css('div.h3_title::text').extract_first()
            for element in chart.css('div.chartAreaContainer div.grid'):
                element_name = (Selector(text=element.css('::attr(data-content)').extract_first()).css('b::text').extract_first() or 
                                element.css('::attr(data-content)').extract_first())
                # import ipdb; ipdb.set_trace()
                chart_data.update({element_name: element.css('::attr(data-value)').extract_first()})
            charts_data.update({chart_name: chart_data})
        data_dict['charts_info'] = charts_data
        yield data_dict

        self.company = companies.pop()
        yield SplashRequest(f'https://clutch.co{(self.company["url"])}', self.parse, dont_filter=True, args={'wait': 1.5})
