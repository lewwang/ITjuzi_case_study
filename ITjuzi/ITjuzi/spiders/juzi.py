import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TCPTimedOutError

from ITjuzi.settings import JUZI_PWD, JUZI_USER
from ITjuzi.items import ItjuziItem
import json


class JuziSpider(scrapy.Spider):
    name = 'juzi'
    allowed_domains = ['itjuzi.com']

    def start_requests(self):
        """
        先登录桔子网
        """
        url = "https://www.itjuzi.com/api/authorizations"
        payload = {"account": JUZI_USER, "password": JUZI_PWD, "type": "pswd"}
        # 提交json数据不能用scrapy.FormRequest，需要使用scrapy.Request，然后需要method、headers参数

        yield scrapy.Request(url=url,
                             method="POST",
                             body=json.dumps(payload),
                             headers={'Content-Type': 'application/json'},
                             callback=self.parse
                             )

    def parse(self, response):
        # 获取Authorization参数的值
        token = json.loads(response.text)
        url = "https://www.itjuzi.com/api/persons"
        payload = {"total": 0, "per_page": 20, "page": 1, "scope": [], "sub_scope": "", "round": [], "prov": "",
                   "city": [], "status": "", "type": 1, "selected": "", "location": "", "hot_city": ""}

        yield scrapy.Request(url=url,
                             method="POST",
                             body=json.dumps(payload),
                             meta={'token': token},
                             # 把Authorization参数放到headers中
                             headers={'Content-Type': 'application/json', 'Authorization': token['data']['token']},
                             callback=self.parse_info
                             )

    def parse_info(self, response):
        # 获取传递的Authorization参数的值
        token = response.meta["token"]
        # 获取总记录数
        total = json.loads(response.text)["data"]["page"]["total"]
        # 因为每页20条数据，所以可以算出一共有多少页
        if type(int(total) / 20) is not int:
            page = int(int(total) / 20) + 1
        else:
            page = int(total) / 20

        url = "https://www.itjuzi.com/api/persons"
        for i in range(1, page + 1):
            # 1431已爬
            if i <= 1431:
                continue
            payload = {"total": total, "per_page": 20, "page": i, "scope": [], "sub_scope": "", "round": [],
                       "prov": "", "city": [], "status": "", "type": 1, "selected": "", "location": "", "hot_city": ""}
            yield scrapy.Request(url=url,
                                 method="POST",
                                 body=json.dumps(payload),
                                 headers={'Content-Type': 'application/json', 'Authorization': token['data']['token']},
                                 callback=self.parse_detail
                                 )

    def parse_detail(self, response):
        try:
            infos = json.loads(response.text)["data"]["data"]
            for i in infos:
                item = ItjuziItem()
                item["city"] = i["city"]
                item["com_claim"] = i["com_claim"]
                item["com_history"] = i["com_history"]
                item["com_round"] = i["com_round"]
                item["com_scope"] = i["com_scope"]
                item["combo_make_com"] = i["combo_make_com"]
                item["des"] = i["des"]
                item["education"] = i["education"]
                item["famous_com"] = i["famous_com"]
                item["famous_school"] = i["famous_school"]
                item["follow_num"] = i["follow_num"]
                item["follow_status"] = i["follow_status"]
                item["id"] = i["id"]
                item["invse_history"] = i["invse_history"]
                item["invse_round"] = i["invse_round"]
                item["invse_scope"] = i["invse_scope"]
                item["invst_claim"] = i["invst_claim"]
                item["invst_history"] = i["invst_history"]
                item["job"] = i["job"]
                item["location"] = i["location"]
                item["logo"] = i["logo"]
                item["name"] = i["name"]
                item["prov"] = i["prov"]
                item["type"] = i["type"]

                yield item
        except Exception as e:
            self.log(e)
