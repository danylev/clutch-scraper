import scrapy
from scrapy import Selector

from scrapy_splash import SplashRequest

class ClutchListSpider(scrapy.Spider):
    name = "clutch-rating"
    start_urls = [
        'https://clutch.co/web-developers/research',
        'https://clutch.co/agencies/leaders-matrix',
        'https://clutch.co/agencies/digital-marketing/leaders-matrix',
        'https://clutch.co/agencies/social-media-marketing/research',
        'https://clutch.co/agencies/app-marketing/research',
        'https://clutch.co/agencies/content-marketing/research',
        'https://clutch.co/agencies/digital/leaders-matrix',
        'https://clutch.co/agencies/creative/leaders-matrix',
        'https://clutch.co/agencies/branding/research',
        'https://clutch.co/agencies/naming/research',
        'https://clutch.co/agencies/video-production/leaders-matrix',
        'https://clutch.co/pr-firms/leaders-matrix',
        'https://clutch.co/agencies/media-buying/leaders-matrix',
        'https://clutch.co/agencies/digital-strategy/research',
        'https://clutch.co/agencies/email/leaders-matrix',
        'https://clutch.co/agencies/inbound-marketing/leaders-matrix',
        'https://clutch.co/agencies/market-research/leaders-matrix',
        'https://clutch.co/seo-firms/research',
        'https://clutch.co/agencies/ppc/research',
        'https://clutch.co/agencies/sem/research',
        'https://clutch.co/research/top-mobile-application-developers',
        'https://clutch.co/research/top-android-application-developers',
        'https://clutch.co/research/top-iphone-application-developers',
        'https://clutch.co/web-developers/research',
        'https://clutch.co/developers/research',
        'https://clutch.co/developers/ecommerce/research',
        'https://clutch.co/developers/dot-net/research',
        'https://clutch.co/developers/virtual-reality/leaders-matrix',
        'https://clutch.co/developers/artificial-intelligence/leaders-matrix',
        'https://clutch.co/developers/blockchain/leaders-matrix',
        'https://clutch.co/developers/drupal/research',
        'https://clutch.co/developers/internet-of-things/leaders-matrix',
        'https://clutch.co/developers/magento/research',
        'https://clutch.co/web-developers/php/leaders-matrix',
        'https://clutch.co/developers/ruby-rails/research',
        'https://clutch.co/developers/shopify/research',
        'https://clutch.co/developers/wordpress/research',
        'https://clutch.co/web-designers/research',
        'https://clutch.co/agencies/ui-ux/research',
        'https://clutch.co/agencies/digital-design/research',
        'https://clutch.co/agencies/graphic-designers/leaders-matrix',
        'https://clutch.co/agencies/logo-designers/leaders-matrix',
        'https://clutch.co/agencies/product-design/leaders-matrix',
        'https://clutch.co/agencies/design/leaders-matrix',
        'https://clutch.co/agencies/packaging-design/leaders-matrix',
        'https://clutch.co/agencies/print-design/leaders-matrix',
        'https://clutch.co/it-services/msp/leaders-matrix',
        'https://clutch.co/it-services#leaders-matrix',
        'https://clutch.co/it-services/analytics/leaders-matrix',
        'https://clutch.co/it-services/cloud/leaders-matrix',
        'https://clutch.co/it-services/cybersecurity/leaders-matrix',
        'https://clutch.co/it-services/staff-augmentation/leaders-matrix',
        'https://clutch.co/bpo/leaders-matrix',
        'https://clutch.co/call-centers/leaders-matrix',
        'https://clutch.co/call-centers/telemarketing/leaders-matrix',
        'https://clutch.co/consulting/leaders-matrix',
        'https://clutch.co/accounting/leaders-matrix',
        'https://clutch.co/hr/leaders-matrix',
        'https://clutch.co/call-centers/answering-services/leaders-matrix',
        
    ]


    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 2.0})

    def parse(self, response):
        for company in response.css('div.provider-row'):
            company_name: str = company.css(str('h3.company-name > a::text')).extract_first()
            company_nid: str = company.css('div.row::attr(id)').extract_first().split('-')[-1] 
            company_url: str = company.css('h3.company-name > a::attr("href")').extract_first()
            ability_to_deliver, focus_chart = company.css('div.chartAreaWrapper')
            focus_dict: dict = {}
            delivery_dict: dict = {}
            if focus_chart:
                for element in focus_chart.css('div.grid'):
                    focus_dict.update({element.css('span::attr(data-content)').extract_first() or 'Other': 
                                       element.css('div.value::text').extract_first().split()[0]})
            if ability_to_deliver:
                for element in ability_to_deliver.css('div.Grid'):
                    delivery_dict.update({element.css('::attr(data-content)').extract_first() or 'Other': 
                                       element.css('div.value::text').extract_first().split()[0]})
            data_dict = {
                'name': company_name.strip() if company_name else None,
                'nid': company_nid.strip() if company_nid else None, 
                'url': company_url.strip() if company_url else None,
                'focus': focus_dict,
                'ability_to_deliver': delivery_dict,
            }
            yield data_dict
