import re
import random
import logging
from scrapyeasy.mymiddlewares import getproxies
from scrapy.exceptions import CloseSpider

log = logging.getLogger('scrapy.randomproxy')

class Mode:
    RANDOMIZE_PROXY_EVERY_REQUESTS, RANDOMIZE_PROXY_ONCE = range(2)

class RandomProxy(object):
    def __init__(self, settings):
        self.mode = settings.get('PROXY_MODE')
        self.chosen_proxy = ''

        if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS or self.mode == Mode.RANDOMIZE_PROXY_ONCE:
            # 获取proxies
            self.proxies = {}
            self.proxies.update(getproxies.get_proxies(settings.get('MIN_PROXIES')))

            if len(self.proxies) == 0:
                raise ValueError('do not get proxies')

            if self.mode == Mode.RANDOMIZE_PROXY_ONCE:
                self.chosen_proxy = random.choice(list(self.proxies.keys()))

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        # Don't overwrite with a random one (server-side state for IP)
        # if request has change_proxy meta, fail num +1
        if 'proxy' in request.meta:
            if request.meta["exception"] is False:
                return
        if 'change_proxy' in request.meta:
            if request.meta['change_proxy'] == True:
                proxy = request.meta['proxy']
                try:
                    self.proxies[proxy] += 1
                except KeyError:
                    pass
                log.debug('%s fail num +1, now %d' % (proxy,int(self.proxies[proxy])))
        request.meta["exception"] = False

        # if proxies less than MIN_PROXIES, get new proxies
        if len(self.proxies) < spider.settings['MIN_PROXIES']:
            self.proxies.update(getproxies.get_proxies(spider.settings['GET_PROXIES_NUM']))
            log.debug('get new proxy, %d proxies left' % len(self.proxies))
        # if proxies == 0 ,close the spider
        if len(self.proxies) == 0:
            raise CloseSpider('All proxies are unusable, cannot proceed')
        # change random proxy every request
        if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS:
            proxy_address = random.choice(list(self.proxies.keys()))
        else:
            proxy_address = self.chosen_proxy

        # if fail num <= PROXY MAX FAIL, fail num +1, if >= ,remove the proxy
        if self.proxies[proxy_address] <= spider.settings['PROXY_MAX_FAIL']:
            request.meta['proxy'] = proxy_address
        else:
            try:
                del self.proxies[proxy_address]
            except KeyError:
                pass
            log.debug('fail > %s, delete %s, %d proxies left' % (spider.settings['PROXY_MAX_FAIL'], proxy_address, len(self.proxies)))
        log.debug('Using proxy <%s>, fail = %s, %d proxies left' % (
                proxy_address, self.proxies[proxy_address], len(self.proxies)))

    def process_exception(self, request, exception, spider):
        if 'proxy' not in request.meta:
            return
        if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS or self.mode == Mode.RANDOMIZE_PROXY_ONCE:
            proxy = request.meta['proxy']

            if self.proxies.get(proxy):
                if self.proxies.get(proxy) >= spider.settings['PROXY_MAX_FAIL']:
                    try:
                        del self.proxies[proxy]
                    except KeyError:
                        pass
                else:
                    self.proxies[proxy] += 1

            request.meta["exception"] = True
            if self.mode == Mode.RANDOMIZE_PROXY_ONCE:
                self.chosen_proxy = random.choice(list(self.proxies.keys()))
            log.info('proxy <%s> failed +1, %d proxies left' % (
                proxy, len(self.proxies)))
