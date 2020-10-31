# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EtherscanItem(scrapy.Item):
    '''Fields to monitor'''
    name = scrapy.Field()
    usd_price = scrapy.Field()
    eth_price = scrapy.Field()
    change = scrapy.Field()
    volume = scrapy.Field()
    market_cap = scrapy.Field()
    holders = scrapy.Field()
    token_page = scrapy.Field()

    '''Fields to get once'''
    total_supply = scrapy.Field()
    contract = scrapy.Field()
    official_website = scrapy.Field()
    social_profile = scrapy.Field()