# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql


class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1", user="root", passwd="123456", db="sbiao_data", charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        def if_key(key):
            if dict(item).has_key(key):
                return item[key]
            return ''

        insert_sql = """
                    insert into qda_shi( title, apply_num, sbiao_category, apply_date, url,
                                          apply_name_ch, apply_name_en, apply_addr_ch, apply_addr_en,
                                          image_url, image_detail, service_list, trial_ann_num,
                                          trial_ann_date, reg_ann_num, reg_ann_date, special_date,
                                          if_comm_sbiao, late_date, inter_reg_date, priority_date,
                                          agent_name, sbiao_status, sbiao_announce, present_status
                                          )
                    values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        self.cursor.execute(insert_sql,
                            (if_key("title"), if_key("apply_num"), if_key("sbiao_category"), if_key("apply_date"),
                             if_key("url"),
                             if_key("apply_name_ch"), if_key("apply_name_en"), if_key("apply_addr_ch"),
                             if_key("apply_addr_en"),
                             if_key("image_url"), if_key("image_detail"), if_key("service_list"),
                             if_key("trial_ann_num"),
                             if_key("trial_ann_date"), if_key("reg_ann_num"), if_key("reg_ann_date"),
                             if_key("special_date"),
                             if_key("if_comm_sbiao"), if_key("late_date"), if_key("inter_reg_date"),
                             if_key("priority_date"),
                             if_key("agent_name"), if_key("sbiao_status"), if_key("sbiao_announce"),
                             if_key("present_status")
                             ))
        self.conn.commit()
        return item
