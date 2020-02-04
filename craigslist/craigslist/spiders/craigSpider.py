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
        Rule(LinkExtractor(restrict_xpaths="//a[@class='pet']"), follow=True),
        Rule(LinkExtractor(restrict_xpaths="//ul[@class='rows']/li/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//a[@class='button next']"), follow=True) 
    )

    def parse_item(self, response):
        bodyObject = response.xpath("//section[@id='postingbody']/text()").getall()

        s = ' '
        body = s.join(bodyObject)
        
        yield {
            'title': response.xpath("normalize-space(//span[@id='titletextonly']/text())").get(),
            'body': body,
            'location': response.xpath("//span[@class='postingtitletext']/small/text()").get(),
            'map_url': response.xpath("//div[@class='mapbox']/p[@class='mapaddress']/small/a/@href").get(),
            'url': response.url
        }
        
