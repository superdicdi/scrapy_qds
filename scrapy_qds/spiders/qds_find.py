# -*- coding: utf-8 -*-

import urlparse
import scrapy
from selenium import webdriver
import time

from scrapy_qds.items import ScrapyQdsItemLoader, ScrapyQdsItem


class QdsFindSpider(scrapy.Spider):
    name = 'qds_find'
    allowed_domains = ['www.quandashi.com']
    start_urls = ['https://www.quandashi.com/']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    def start_requests(self):
        url = "https://account.quandashi.com/passport/login?callback=https%3A%2F%2Fwww.quandashi.com%2F"
        driver = webdriver.Chrome(executable_path='E:\Develop\chromedriver_win32\chromedriver.exe')
        driver.get(url)
        time.sleep(5)  # 延时操作等网页加载完毕再去获取字段
        driver.find_element_by_xpath('//*[@id="username"]').send_keys("用户名")
        driver.find_element_by_xpath('//input[@type="password"]').send_keys("密码")
        driver.find_element_by_xpath('//*[@id="btn-login"]').click()
        time.sleep(15)
        cookie = driver.get_cookies()  # 获取登录后的 cookies
        yield scrapy.Request(url="https://so.quandashi.com/index/search?key=查询关键字",
                             headers=self.headers, dont_filter=True, cookies=cookie, meta={"cookie": cookie})

    def parse(self, response):
        dl_nodes = response.xpath('//div[@class="searchLis-result"]/dl')
        next_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        cookie = response.meta.get("cookie", "")
        for node in dl_nodes:
            detail_url = node.xpath('dt/span/a/@href').extract_first()
            present_status = node.xpath('dd/table/tr[@class="row-2"]/td[1]/a/i/text()').extract_first()
            yield scrapy.Request(url=urlparse.urljoin(response.url, detail_url), headers=self.headers, dont_filter=True,
                                 cookies=cookie, meta={"cookie": cookie, "present_status": present_status},
                                 callback=self.parse_detail)
        if next_url:
            yield scrapy.Request(url=urlparse.urljoin(response.url, next_url), headers=self.headers, dont_filter=True,
                                 cookies=cookie, meta={"cookie": cookie}, callback=self.parse)

    def parse_detail(self, response):
        item_loader = ScrapyQdsItemLoader(item=ScrapyQdsItem(), response=response)
        item_loader.add_xpath('title',          '//div[@class="searchDetail-wrap"]/table[1]/tr[1]/td[2]/i/text()')
        item_loader.add_xpath('apply_num',      '//div[@class="searchDetail-wrap"]/table[1]/tr[2]/td[2]/text()')
        item_loader.add_xpath('sbiao_category', '//div[@class="searchDetail-wrap"]/table[1]/tr[2]/td[4]/text()')
        item_loader.add_xpath('apply_date',     '//div[@class="searchDetail-wrap"]/table[1]/tr[2]/td[6]/text()')
        item_loader.add_xpath('apply_name_ch',  '//div[@class="searchDetail-wrap"]/table[1]/tr[3]/td[2]/a/i/text()')
        item_loader.add_xpath('apply_addr_ch',  '//div[@class="searchDetail-wrap"]/table[1]/tr[4]/td[2]/text()')
        item_loader.add_xpath('apply_name_en',  '//div[@class="searchDetail-wrap"]/table[1]/tr[5]/td[2]/text()')
        item_loader.add_xpath('apply_addr_en',  '//div[@class="searchDetail-wrap"]/table[1]/tr[5]/td[4]/text()')
        item_loader.add_xpath('image_url',      '//div[@class="searchDetail-wrap"]/table[2]/tr[1]/td[2]/div/img/@src')
        item_loader.add_xpath('image_detail',   '//div[@class="searchDetail-wrap"]/table[2]/tr[1]/td[4]/ul/text()')
        item_loader.add_xpath('service_list',   '//div[@class="searchDetail-wrap"]/table[2]/tr[2]/td[2]/ul/li/text()')
        item_loader.add_xpath('trial_ann_num',  '//div[@class="searchDetail-wrap"]/table[3]/tr[1]/td[2]/text()')
        item_loader.add_xpath('reg_ann_num',    '//div[@class="searchDetail-wrap"]/table[3]/tr[1]/td[4]/text()')
        item_loader.add_xpath('trial_ann_date', '//div[@class="searchDetail-wrap"]/table[3]/tr[2]/td[2]/text()')
        item_loader.add_xpath('reg_ann_date',   '//div[@class="searchDetail-wrap"]/table[3]/tr[2]/td[4]/text()')
        item_loader.add_xpath('special_date',   '//div[@class="searchDetail-wrap"]/table[3]/tr[3]/td[2]/text()')
        item_loader.add_xpath('if_comm_sbiao',  '//div[@class="searchDetail-wrap"]/table[3]/tr[3]/td[4]/text()')
        item_loader.add_xpath('late_date',      '//div[@class="searchDetail-wrap"]/table[3]/tr[4]/td[2]/text()')
        item_loader.add_xpath('inter_reg_date', '//div[@class="searchDetail-wrap"]/table[3]/tr[4]/td[4]/text()')
        item_loader.add_xpath('priority_date',  '//div[@class="searchDetail-wrap"]/table[3]/tr[5]/td[2]/text()')
        item_loader.add_xpath('agent_name',     '//div[@class="searchDetail-wrap"]/table[3]/tr[5]/td[4]/a/text()')
        item_loader.add_xpath('sbiao_status',   '//div[@class="searchDetail-wrap"]/table[3]/tr[6]/td[2]/ul/li/text()')
        item_loader.add_xpath('sbiao_announce', '//div[@class="searchDetail-wrap"]/table[3]/tr[7]/td[2]/ul/li/text()')
        item_loader.add_value('present_status', response.meta.get("present_status", ""))
        item_loader.add_value('url', response.url)
        qda_shi_item = item_loader.load_item()
        yield qda_shi_item