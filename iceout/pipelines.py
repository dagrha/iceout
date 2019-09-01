# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3


class SQLitePipeline(object):
    def open_spider(self, spider):
        db = spider.settings.get('SQLITE_DB')
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS iceouts (lake_id INT NOT NULL, iceout DATE, source TEXT, comment TEXT);''')

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    def insert_db(self, item):
        values = (
            item['lake_id'],
            item['iceout'],
            item['source'],
            item['comment'],
        )

        cmd = """INSERT INTO iceouts (lake_id, iceout, source, comment) VALUES(?, ?, ?, ?)"""
        self.cur.execute(cmd, values)