# -*- coding: utf-8 -*-
import scrapy


class GlassesSpider(scrapy.Spider):
    name = 'glasses'
    allowed_domains = ['glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers']

    def parse(self, response):
        # we want: product url, product image url, product name, product price
        
        # get and yield all glasses on current page
        glassesList = response.xpath("//div[@class='col-sm-6 col-md-4 m-p-product']")

        for g in glassesList:
            productUrl = g.xpath(".//div/a/@href").get()
            imageUrl = g.xpath(".//div/a/img/@src").get()
            productName = g.xpath(".//div[2]/p/a/text()").get()
            productPrice = g.xpath(".//div[2]/div/span/text()").get()
            discountedPrice = g.xpath(".//div[2]/div/span/span/text()").get()

            if discountedPrice:
                productPrice = discountedPrice

            yield {
                'product_name': productName,
                'product_price': productPrice,
                'product_url': productUrl,
                'image_url': imageUrl                
            }

        # check if a next page exists if so set url = nextpage href and callback to parse function
        nextPage = response.xpath("//a[@rel='next']/@href").get()

        if nextPage:
            yield scrapy.Request(url=nextPage, callback=self.parse)