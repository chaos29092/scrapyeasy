# -*-coding:utf-8-*-
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from fake_useragent import UserAgent


class RotateUserAgentDesktopMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = UserAgent()
        now_ua = ua.random

        while 'Mobile' in now_ua:
            now_ua = ua.random

        request.headers.setdefault('User-Agent', now_ua)

class RotateUserAgentMobileMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = UserAgent()
        now_ua = ua.random

        while 'Mobile' not in now_ua:
            now_ua = ua.random

        request.headers.setdefault('User-Agent', now_ua)