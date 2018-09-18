# -*- coding: utf-8 -*-
#Crawl frequency setting 8 DOMAIN 8 REQUESTS
#use alibaba suppliers url list crawl alibaba suppliers detail
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapyeasy.items import exampleItem
import logging
import re

log = logging.getLogger('spider')

class scrapyeasySpider(CrawlSpider):
    name = "scrapyeasy"
    allowed_domains = ["scrapyeasy.com"]
    # input start_urls by file
    url_list = []
    with open('/home/chaos/Desktop/1', 'r') as f:
        for line in f.readlines():
            url_list.append(line.strip())

    # 自己组合urls列表
    # for i in range(4000,16000):
    #     url_list.append('http://www.scrapyeasy.com/page_'+str(i)+'_a.html')
    start_urls = url_list
    # or use tuple
    # start_urls = ['http://m.scrapyeasy.com/lists']

    custom_settings = {
        'ITEM_PIPELINES':{
            'scrapyeasy.pipelines.examplePipeline': 300,
            },
        # 'CONCURRENT_REQUESTS': 200,
        # 'DEPTH_LIMIT': 1,
        # 'COOKIES_ENABLED': False,
        # 'RETRY_ENABLED' : False,
        # 'DOWNLOAD_TIMEOUT': 30,
        # 'REDIRECT_ENABLED' : False,
    }

    rules = (
        # 翻页
        Rule(LinkExtractor(allow=('/list_1','/list_2'))),
        # 抓取内页信息
        Rule(LinkExtractor(allow=('/pagedetail/')),callback='parse_item'),
    )

    # 如果需要抓取start_urls上的item，则需要重写这个函数
    # def parse_start_url(self, response):
    #     return self.parse_item(response)

    def parse_item(self, response):
        # 检测是否被封，如果被封，则换ip
        if (re.match('The system', response.selector.xpath('string(body)').extract_first())):
            req = response.request
            req.meta["change_proxy"] = True
            yield scrapy.Request(url=response.url, dont_filter=True)
            # 测试是否触发这个if的时候用
            log.info('111')
        else:
            loader = ItemLoader(exampleItem(), response=response)

            loader.add_value('url', response.url)
            loader.add_xpath('name', '//h2/text()')
            loader.add_xpath('cas', '//li/span[contains(.,"CAS:")]/../text()')
            # 选择文字包含Synonyms的span的上级节点的兄弟节点
            loader.add_xpath('synonyms','//span[contains(.,"Synonyms")]/../following-sibling::a/text()')
            # 也可以抓取并储存一个数组
            loader.add_xpath('next_url','//ul/li/a/@href')

            for sel in response.xpath('/div[@class="css"]'):
                # .//代表以sel为基准来选择sel以下的所有满足条件的，//代表从全局来选择，没有前缀则需要一层一层的准确选择
                loader.add_value('a1',sel.xpath('.//h2/text()').extract_first())

            yield loader.load_item()

    # 这是一个自定义初始requests，然后压入抓取队列的例子
    # def start_requests(self):
    #     for u in self.start_urls:
    #         yield scrapy.Request(u, callback=self.parse_httpbin,
    #                              errback=self.errback_httpbin,
    #                              dont_filter=True)