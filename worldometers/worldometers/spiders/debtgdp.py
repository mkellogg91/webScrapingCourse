# -*- coding: utf-8 -*-
import scrapy


class DebtgdpSpider(scrapy.Spider):
    name = 'debtgdp'
    allowed_domains = ['www.worldpopulationreview.com']
    start_urls = ['http://worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        countries = response.xpath("//table[@class='table table-striped']/tbody/tr")

        for country in countries:
            name = country.xpath(".//td[1]/a/text()").get()
            gdp = country.xpath(".//td[2]/text()").get()

            yield {
                'country': name,
                'gdp': gdp    
            }
        