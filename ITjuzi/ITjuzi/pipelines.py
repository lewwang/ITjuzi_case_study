# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from ITjuzi.settings import DATABASE_DB, DATABASE_HOST, DATABASE_PORT, DATABASE_PWD, DATABASE_USER
import pymysql

class ItjuziPipeline:

    def __init__(self):
        host = DATABASE_HOST
        port = DATABASE_PORT
        user = DATABASE_USER
        passwd = DATABASE_PWD
        db = DATABASE_DB
        try:
            self.conn = pymysql.Connect(host=host, port=port, user=user, passwd=passwd, db=db, charset='utf8')
        except Exception as e:
            print("连接数据库出错,错误原因%s" % e)
            raise e
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        params = [item['id'], item['city'], item['com_claim'], str(item['com_history']),
                  str(item['com_round']), str(item['com_scope']), item['combo_make_com'], item['des'], str(item['education']), item['famous_com'],
                  item['famous_school'], item['follow_num'], item['follow_status'], str(item['invse_history']), str(item['invse_round']),
                  str(item['invse_scope']), item['invst_claim'], str(item['invst_history']), str(item['job']), item['location'], item['logo'],
                  item['name'], item['prov'], str(item['type'])]
        try:
            _ = self.cur.execute(
                '''
                replace into itjuzi_entrepreneur(id, city, com_claim, com_history, com_round, com_scope, combo_make_com, des,
                    education, famous_com, famous_school, follow_num, follow_status, invse_history, invse_round, invse_scope,
                    invst_claim, invst_history, job, location, logo, name, prov, type) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ''', tuple(params))

            self.conn.commit()
        except Exception as e:
            print("插入数据出错,错误原因%s" % e)
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()


