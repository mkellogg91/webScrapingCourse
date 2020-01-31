# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CraigspiderSpider(CrawlSpider):
    name = 'craigSpider'
    allowed_domains = ['craigslist.org']
    start_urls = ['https://www.craigslist.org/about/sites']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='colmask'][1]/div/ul/li/a"), follow=True),
        Rule(LinkExtractor(restrict_xpaths="//div[@id='ccc']/h4/a"), follow=True),
        Rule(LinkExtractor(restrict_xpaths="//ul[@class='rows']/li/a"), callback='parse_item', follow=True),
        
    )

    def parse_item(self, response):
        yield {
            'title': response.xpath("normalize-space(//span[@id='titletextonly']/text())").get(),
            'location': response.xpath("//span[@class='postingtitletext']/small/text()").get(),
            'map_url': response.xpath("//div[@class='mapbox']/p[@class='mapaddress']/small/a/@href").get(),
            'body': response.xpath("normalize-space(//section[@id='postingbody']/text())").get(),
            'url': response.url
        }
        
