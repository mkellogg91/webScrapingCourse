# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo
import sqlite3

class MongodbPipeline(object):
    collection_name = "pet_posts"

    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb+srv://user:altec1991@cluster0-a1j7v.mongodb.net/test?retryWrites=true&w=majority")
        self.db = self.client["CRAIG"]
    
    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item

class SQLlitePipeline(object):

    def open_spider(self, spider):
        self.connection = sqlite3.connect("craig.db")
        self.c = self.connection.cursor()
        self.c.execute('''
            CREATE TABLE pet_items(
                title TEXT,
                body TEXT,
                location TEXT,
                map_url TEXT,
                url TEXT
            )
        ''')
        self.connection.commit()
    
    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO pet_items (title, body, location, map_url, url) VALUES(?,?,?,?,?)
        ''', (
            item.get('title'),
            item.get('body'),
            item.get('location'),
            item.get('map_url'),
            item.get('url')
        ))
        self.connection.commit()
        return item