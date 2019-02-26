# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request,FormRequest


class YishouSpider(scrapy.Spider):
    name = 'yishou'
    allowed_domains = ['api.yishouapp.com']
    start_urls = ['http://api.yishouapp.com/']

    def __init__(self):
        self.headers = {
                "User-Agent": "Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Host': 'api.yishouapp.com',
                'Upgrade-Insecure-Requests': '1',
            }

        self.uid = "1615579"
        self.token = "b21c0be7a26fde584cf3ee531d8b5b3c"
        self.udid = "863654029144979"
        self.url = "https://api.yishouapp.com/goods/get_goods_info"


    def start_requests(self):

        # cat_list = ["296", "297", "299", "300", "302"]
        cat_list = ["296"]
        for cat_id in cat_list:
            data = {
                "version_name": "3.4.1",
                "uid": self.uid,
                # "cat_id": "297", # 产品类别编号
                "cat_id": cat_id,  # 产品类别编号
                "token": self.token,
                # "page": page,
                "page": "1",
                "_abtest": "1",
                "udid": self.udid,
                "plat_type": "Android",
                "version_code": "341"
            }

            body = "version_name=3.4.1&uid={}&cat_id={}&token={}&page={}&_abtest=1&udid=1&plat_type=Android&version_code=341".format(self.uid, cat_id, self.token, self.udid)

            # return Request(url=self.url, headers=self.headers, method="POST", body=body, callback=self.get_id, meta={"cat_id": cat_id},dont_filter=True)
            yield Request(url=self.url, headers=self.headers, method="POST", body=body, callback=self.get_id, meta={"cat_id": cat_id},dont_filter=True)
            # return FormRequest(url=self.url, headers=self.headers, method="POST", formdata=data, callback=self.get_id, meta={"cat_id": cat_id}, dont_filter = True)

    def get_pages(self, response):
        html = json.loads(response.text)
        pages = html["data"]["page_total"]
        print(pages)
        cat_id = response.meta["cat_id"]
        # for page in range(1, int(pages) + 1):
        for page in range(1, 2):

            data = {
                "version_name": "3.4.1",
                "uid": self.uid,
                # "cat_id": "297",  # 产品类别编号
                "cat_id": str(cat_id),
                "token": self.token,
                "page": page,
                "_abtest": "1",
                "udid": self.udid,
                "plat_type": "Android",
                "version_code": "341"
                }

            # return Request(url=self.url, headers=self.headers, method="POST", body=data, callback=self.get_id)
            return FormRequest(url=self.url, headers=self.headers, method="POST", fromdata=data, callback=self.get_id, dont_filter = True)

    def get_id(self, response):

        url = "https://api.yishouapp.com/goods/get_goods_info"
        html = json.loads(response.text)
        goods_list_1 = html["data"]["goods_list"]
        # goods_id_list = []
        for goods_ids in goods_list_1:
            goods_id = goods_ids["goods_id"]
            # shop_price=goods_ids["shop_price"]
            # goods_img_url = goods_ids["goods_img"]
            # goods_id_list.append(goods_id)

            with open("./GoodsID.txt", "a+") as fh:
                fh.write(goods_id + "\n")


            data = {
                "version_name": "3.4.1",
                "uid": self.uid,
                "source": "8",
                "token": self.token,
                "_abtest": "1",
                "goods_id": goods_id,
                # "goods_id": "7671071",
                "udid": self.udid,
                "plat_type": "Android",
                "version_code": "341",
                "ss_type": "0"
            }

            # return Request(url=url, headers=self.headers, method="POST", body=data, callback=self.get_detali)
            # yield Request(url=url, headers=self.headers, method="POST", body=data, callback=self.get_detali,)
            # yield FormRequest(url=url, headers=self.headers, method="POST", formdata=data, callback=self.get_detali,dont_filter = True)
            return FormRequest(url=url, headers=self.headers, method="POST", formdata=data, callback=self.get_detali,dont_filter = True)


    def get_detali(self, response):
        html = json.loads(response.text)
        goods_thumb = html["data"]["goods_thumb"]
        goods_images = html["data"]["goods_img"]
        goods_desc = html["data"][
            "goods_desc"]  # "秋冬季节不同品类的排单时长如下：若档口没有库存，一般情况下上衣、裤子、半裙、鞋包配饰排单3-5天，连衣裙和一般的外套7天左右，手工缝制的羊毛大衣7-15天。若遇重工艺的服装加工，则需要多加2-3天；若遇面料排单，则时间会需要顺延；若面料缺货，则会面临缺货。"
        cat_name = html["data"]["cat_name"]  # 蕾丝/雪纺衫
        fabric = html["data"]["fabric_tag"]  # 雪纺
        origin_name = html["data"]["origin_name"]  # 广州发货商品

        # 颜色分类
        attributes = html["data"]["attribute"]
        for attribute in attributes:
            color = attribute["color"]  # 灰色
            color_card = attribute["color_card"]  # 商品大图
            card_thumb = attribute["card_thumb"]  # 商品小图

            items = attribute["item"]
            for item in items:
                size = item["size"]  # 均码
                sort = item["sort"]  # 194
                stock = item["stock"]  # 500
                sku = item["sku"]  # 16217830

            print(color, color_card, card_thumb, size, sort, stock, sku)

        goods_name = html["data"]["goods_name"]  # "【ANGEL KISS】性感百搭一字肩镂空雪纺衫 8023-1# LXX"
        shop_price = html["data"]["shop_price"]  # 47.25
        special_end_time = html["data"]["special_end_time"]  # 限时秒杀剩余时间？1550790000

        goods_tags = html["data"]["goods_tags"]  # "山河南城"，"ANGEL KISS"，"面料舒适"
        colors = html["data"]["color"]
        size = html["data"]["size"]

        print(goods_thumb, goods_images, goods_desc, cat_name, fabric, origin_name, goods_name, shop_price,
              special_end_time, goods_tags, colors, size)

    # def parse(self, response):
    #     pass

