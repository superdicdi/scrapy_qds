# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, MapCompose


def remove_char(value):
    # 去除包含的换行符、分隔符、制表符和空格，不然将数据导出成 Excel 文件的时候会出现大片空格和换行
    return value.replace('\n', "").replace('\r', "").replace('\t', "").replace(" ", "")


class ScrapyQdsItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(remove_char)


class ScrapyQdsItem(scrapy.Item):
    title = scrapy.Field()  # 商标名称
    apply_num = scrapy.Field()  # 申请号
    sbiao_category = scrapy.Field()  # 商标类别
    apply_date = scrapy.Field()  # 申请日期
    apply_name_ch = scrapy.Field()  # 申请人名称（中文）
    apply_name_en = scrapy.Field()  # 申请人名称（英文）
    apply_addr_ch = scrapy.Field()  # 申请人地址（中文）
    apply_addr_en = scrapy.Field()  # 申请人地址（英文）
    image_url = scrapy.Field()  # 商标logo的url
    image_detail = scrapy.Field()  # 图片要素
    service_list = scrapy.Field(
        output_processor=Join(",")
    )  # 商品/服务列表
    trial_ann_num = scrapy.Field()  # 初审公告期号
    trial_ann_date = scrapy.Field()  # 初审公告日期
    reg_ann_num = scrapy.Field()  # 注册公告期号
    reg_ann_date = scrapy.Field()  # 注册公告日期
    special_date = scrapy.Field()  # 专用权期限
    if_comm_sbiao = scrapy.Field()  # 是否共有商标
    late_date = scrapy.Field()  # 后期指定日期
    inter_reg_date = scrapy.Field()  # 国际注册日期
    priority_date = scrapy.Field()  # 优先权日期
    agent_name = scrapy.Field()  # 代理人名称
    sbiao_status = scrapy.Field(
        output_processor=Join(",")
    )  # 商标状态
    sbiao_announce = scrapy.Field(
        output_processor=Join(",")
    )  # 商标公告
    present_status = scrapy.Field()  # 当前状态
    url = scrapy.Field()  # 详情页的url
