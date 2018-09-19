import re
import random
import logging
from scrapyeasy.mymiddlewares import getproxies
from scrapy.exceptions import CloseSpider

log = logging.getLogger('scrapy.randomproxy')


class RandomProxy(object):
    def __init__(self, settings):
        # 获取proxies
        self.proxies = {}
        self.proxies.update(getproxies.get_proxies(settings.get('MIN_PROXIES')))

        if len(self.proxies) == 0:
            raise ValueError('do not get proxies')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        # if request has change_proxy meta, fail num +1
        if 'proxy' in request.meta:
            if request.meta["exception"] is False:
                return
        if 'change_proxy' in request.meta:
            if request.meta['change_proxy'] == True:
                proxy = request.meta['proxy']
                try:
                    self.proxies[proxy] += 1
                    if self.proxies[proxy] > spider.settings['PROXY_MAX_FAIL']:
                        del self.proxies[proxy]
                except KeyError:
                    pass
                log.debug('%s fail num +1' % (proxy))
        request.meta["exception"] = False

        # if proxies less than MIN_PROXIES, get new proxies
        if len(self.proxies) < spider.settings['MIN_PROXIES']:
            self.proxies.update(getproxies.get_proxies(spider.settings['GET_PROXIES_NUM']))
            log.debug('get new proxy, %d proxies left' % len(self.proxies))
        # if proxies == 0 ,close the spider
        if len(self.proxies) == 0:
            raise CloseSpider('All proxies are unusable, cannot proceed')
        # change random proxy every request
        request.meta['proxy'] = random.choice(list(self.proxies.keys()))

    def process_exception(self, request, exception, spider):
        if 'proxy' not in request.meta:
            return
        proxy = request.meta['proxy']

        if self.proxies.get(proxy):
            if self.proxies.get(proxy) > spider.settings['PROXY_MAX_FAIL']:
                try:
                    del self.proxies[proxy]
                    log.info('delete'+proxy)
                except KeyError:
                    pass
            else:
                self.proxies[proxy] += 1

        request.meta["exception"] = True
