# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/chart/top/?ref_=nv_mv_250']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//tbody/tr/td[@class='titleColumn']/a"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        yield {
            'title': response.xpath("normalize-space(//div[@class='title_wrapper']/h1/text())").get(),
            'year': response.xpath("//div[@class='title_wrapper']/h1/span/a/text()").get(),
            'duration': response.xpath("normalize-space(//div[@class='subtext']/time/text())").get(),
            'genre': response.xpath("//div[@class='subtext']/a[1]/text()").get(),
            'rating': response.xpath("//div[@class='ratingValue']/strong/span/text()").get(),
            'movie_url': response.url,
        }

