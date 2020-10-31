import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urljoin
from scrapy import Selector
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader

from etherscan.items import EtherscanItem

class ethToken(CrawlSpider):
    name = 'token_page'
    start_url = ['https://etherscan.io/tokens']
    rules = (
      Rule(
         LinkExtractor(),
         callback='parse', follow=False),)

    def start_requests(self):
        for each in self.start_url:
            yield SplashRequest(each, callback=self.parse_attr, endpoint='render.html', args={'wait': 4.5})

    def parse_attr(self, response):
        item = EtherscanItem()

        for items in response.xpath('//div[contains(@class, "card-body")]//tr'):
            item['name'] = items.xpath('.//a[contains(@class, "text-primary")]//text()').extract()
            item['usd_price'] = items.xpath('.//td[contains(@class, "text-nowrap")]//text()').extract_first()
            item['eth_price'] = items.xpath('.//td[contains(@class, "text-nowrap")]//span//text()').extract_first()
            item['change'] = items.xpath('.//td[4]//text()').extract_first()
            item['volume'] = items.xpath('.//td[5]//text()').extract_first()
            item['market_cap'] = items.xpath('.//td[6]//text()').extract_first()
            item['holders'] = items.xpath('.//td[7]//text()').extract_first()

            token_page = items.xpath('.//a[contains(@class, "text-primary")]//@href').extract_first()
            token_page = urljoin(response.url, token_page)
            request = SplashRequest(token_page,
                                    callback=self.parse_token_page,
                                    endpoint='render.html',
                                    args={'wait': 3.5},
                                    meta={'item': item},
                                    cb_kwargs=dict(
                                        name=item['name'],
                                        usd_price=item['usd_price'],
                                        eth_price=item['eth_price'],
                                        change=item['change'],
                                        volume=item['volume'],
                                        market_cap=item['market_cap'],
                                        holders=item['holders'],
                                        token_page=token_page))
            request.meta['item'] = item
            yield request


    def parse_token_page(self, response, name, usd_price, eth_price, change, volume, market_cap, holders, token_page):
        item = response.meta['item']
        item['total_supply'] = response.xpath('//div[contains(@id, "ContentPlaceHolder1_divSummary")]//span[contains(@class, "hash-tag text-truncate")]//text()').extract_first()
        item['contract'] = response.xpath('//div[contains(@id, "ContentPlaceHolder1_divSummary")]//div[contains(@class, "card-body")]//div[contains(@class, "d-flex clipboard-hover")]//a//text()').extract_first()
        item['official_website'] = response.xpath('//div[contains(@id, "ContentPlaceHolder1_divSummary")]//div[contains(@class, "card-body")]//div[contains(@id, "ContentPlaceHolder1_tr_officialsite_1")]//div[contains(@class, "col-md-8")]//a//@href').extract_first()
        item['social_profile'] = response.xpath('//div[contains(@id, "ContentPlaceHolder1_divSummary")]//div[contains(@class, "card-body")]//div//div[contains(@class, "row align-items-center")]//div[contains(@class, "col-md-8")]//ul[contains(@class, "list-inline")]//li//@href').extract()


        item['name'] = name
        item['usd_price'] = usd_price
        item['eth_price'] = eth_price
        item['change'] = change
        item['volume'] = volume
        item['market_cap'] = market_cap
        item['holders'] = holders
        item['token_page'] = token_page
        yield item

        BOT_NAME = 'etherscan'

        SPIDER_MODULES = ['etherscan.spiders']
        NEWSPIDER_MODULE = 'etherscan.spiders'
