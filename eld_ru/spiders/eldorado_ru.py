import scrapy
from scrapy.http import HtmlResponse
from parser_goods.items import ParserGoodsItem
from scrapy.loader import ItemLoader


class EldoradoRuSpider(scrapy.Spider):
    name = 'eldorado_ru'
    allowed_domains = ['eldorado.ru']
    
    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        
        self.start_urls = [f"https://www.eldorado.ru/c/televizory/tag/televizory-75-dyujmov/"]

    def parser(self, response:HtmlResponse):
        pages_links = response.xpath("//div[@class='tj -X']//button[contains(@class, 'uj')]")
        for link in pages_links:
            yield response.follow(link, callback=self.parser_goods)

    def parser_goods(self, response:HtmlResponse):
        loader = ItemLoader(item=ParserGoodsItem(), response=response)
        
        loader.add_xpath('article', "//div[@class='tE uE']//span[contains(@class, 'zE')]")
        loader.add_value('url', response.url)
        loader.add_xpath('price', "//div[@class='undefined DQ FQ fG hG']//span[contains(@class, 'IQ PQ')]")
        loader.add_xpath('photos', "//div[@class='tE uE']//img[contains(@class, '_z')]")
        yield loader.load_item()