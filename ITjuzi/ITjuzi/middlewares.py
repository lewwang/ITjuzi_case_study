# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
import json
import requests
import logging
from scrapy import signals
from ITjuzi import settings

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class ItjuziSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ItjuziDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgent(object):
    def __init__(self, user_agent):
        self.user_agent = user_agent
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        # 从settings中加载USER_AGENT的值
        return cls(
            user_agent=crawler.settings.getlist('USER_AGENT')
        )

    def process_request(self, request, spider):
        # 在process_request中设置User-Agent的值
        ua = random.choice(self.user_agent)
        self.logger.debug('======' + '使用ua' + str(ua) + "======")
        request.headers.setdefault('User-Agent', )


class ProxyMiddleware(object):
    def __init__(self, proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url

    def get_random_proxy(self):
        try:
            response = requests.get("{}/get/".format(self.proxy_url))
            if response.status_code == 200:
                self.logger.debug('======' + 'response ' + str(response) + "======")
                proxy = response.json().get("proxy")
                self.logger.debug('======' + 'response ' + str(proxy) + "======")
                ip = {"http": "http://" + proxy, "https": "https://" + proxy}
                r = requests.get("https://www.itjuzi.com/", proxies=ip, timeout=4)
                if r.status_code == 200:
                    return proxy
        except:
            return self.get_random_proxy()

    def process_request(self, request, spider):
        proxy = self.get_random_proxy()
        if proxy:
            self.logger.debug('======' + '使用代理 ' + str(proxy) + "======")
            request.meta['proxy'] = 'https://{proxy}'.format(proxy=proxy)

    def process_response(self, request, response, spider):
        if response.status != 200:
            print("again response ip:")
            request.meta['proxy'] = 'https://{proxy}'.format(proxy=self.get_random_proxy())
            return request
        return response

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL')
        )
