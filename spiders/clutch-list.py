import scrapy
from scrapy import Selector

from scrapy_splash import SplashRequest

class ClutchListSpider(scrapy.Spider):
    name = "clutch-rating"
    start_urls = [
            'https://clutch.co/web-developers?sort_by=field_pp_rank_web_developer&field_pp_min_project_size=All&field_pp_hrly_rate_range=All&field_pp_size_people=All&field_pp_cs_small_biz=&field_pp_cs_midmarket=&field_pp_cs_enterprise=&client_focus=&field_pp_if_advertising=&field_pp_if_automotive=&field_pp_if_arts=&field_pp_if_bizservices=&field_pp_if_conproducts=&field_pp_if_education=&field_pp_if_natural_resources=&field_pp_if_finservices=&field_pp_if_gambling=&field_pp_if_gaming=&field_pp_if_government=&field_pp_if_healthcare=&field_pp_if_hospitality=&field_pp_if_it=&field_pp_if_legal=&field_pp_if_manufacturing=&field_pp_if_media=&field_pp_if_nonprofit=&field_pp_if_realestate=&field_pp_if_retail=&field_pp_if_telecom=&field_pp_if_transportation=&field_pp_if_utilities=&field_pp_if_other=&industry_focus=&field_pp_location_country_select=All&field_pp_location_province=&field_pp_location_latlon_1%5Bpostal_code%5D=&field_pp_location_latlon_1%5Bsearch_distance%5D=100&field_pp_location_latlon_1%5Bsearch_units%5D=mile'
            ]


    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 2})

    def parse(self, response):
        for company in response.css('li.provider-row'):
            company_name: str = company.css('h3.company-name > span > a::text').extract_first()
            company_nid: str = company.css('li.provider-row > div.row::attr(data-clutch-nid)').extract_first() 
            company_url: str = company.css('h3.company-name > span > a::attr("href")').extract_first()
            tagline: str = company.css('p.tagline::text').extract_first().strip()
            rating: str = company.css('span.rating::text').extract_first()
            number_of_reviews: str = company.css('span.reviews-count > a::text').extract_first()
            sponsored: bool = bool(company.css('span.sponsored').extract_first())
            info_box: list =  company.css('div.module-list > div.list-item')
            min_budget: str = info_box[0].css('::text').extract_first()
            hour_rate: str = info_box[1].css('span.hourly-rate::text').extract_first()
            number_of_employees: str = info_box[2].css('span.employees::text').extract_first()
            city: str = info_box[3].css('span.location-city > span.locality::text').extract_first()
            state: str = info_box[3].css('span.location-city > span.region::text').extract_first()
            country: str = info_box[3].css('span.location-country > span.country-name::text').extract_first()
            if city is None:
                data = info_box[3].css('::text').extract_first()
                if data:
                    data = data.split()
                    data = [item.strip() for item in info_box[3].css('::text').extract_first().split(',') if item is not 'none']
                    if data and len(data) > 1:
                        city = data[0]
                        loc = data[1]
                        if len(loc) == 2:
                            state = loc
                        else:
                            country = loc
            focus_chart: list = company.css('div.chartAreaContainer > div.grid')
            focus_dict: dict = {}
            for focus in focus_chart:
                temp_sel_data = focus.css('div::attr(data-content)').extract_first()
                temp_sel = Selector(text=temp_sel_data)
                focus_dict.update({temp_sel.css('b::text').extract_first(): temp_sel.css('i::text').extract_first()})
            data_dict = {
                'name': company_name.strip() if company_name else None,
                'nid': company_nid.strip() if company_nid else None, 
                'url': company_url.strip() if company_url else None,
                'tags': tagline.strip() if tagline else None,
                'focus': focus_dict,
                'rating': rating.strip() if rating else None,
                'reviews': number_of_reviews and number_of_reviews.split()[0],
                'sponsored': sponsored,
                'min_budget': min_budget.strip() if min_budget else None,
                'rate': hour_rate.strip() if hour_rate else None,
                'number_of_employess': number_of_employees.strip() if number_of_employees else None,
                'city': city.strip() if city else None,
                'state': state.strip() if state else None,
                'country': country.strip() if country else "US",
            }
            yield data_dict

        next_page = response.xpath('//*[@id="block-system-main"]/div/div/div/section/div/div/div/div[2]/div/ul/li[3]')[0]
        if next_page is not None:
            # yield response.follow(next_page.css('a::attr("href")').extract_first(), self.parse)
            next_url = next_page.css('a::attr("href")').extract_first()
            yield SplashRequest(f'https://clutch.co{next_url}', self.parse, dont_filter=True, args={'wait': 2})
