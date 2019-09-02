# -*- coding: utf-8 -*-
import scrapy
import json
from iceout.items import IceoutItem


class MnIceoutSpider(scrapy.Spider):
    name = 'mn_iceout'
    ids_url = 'https://maps1.dnr.state.mn.us/cgi-bin/climatology/ice_out_by_year.cgi'

    def start_requests(self):
        yield scrapy.Request(url=self.ids_url, callback=self.parse_json)

    def parse_json(self, response):
        j = json.loads(response.text)
        lake_ids = {i.get('id'): i.get('name') for i in j['results']}
        iceout_url = 'https://maps1.dnr.state.mn.us/cgi-bin/climatology/ice_out_by_lake.cgi?id='
        for lake_id, lake_name in lake_ids.items():
            url = iceout_url + lake_id
            meta = {
                'lake_id': lake_id,
                'lake_name': lake_name,
            }
            yield scrapy.Request(url, callback=self.parse, meta=meta)

    def parse(self, response):
        j = json.loads(response.text)
        lake_id = response.meta.get('lake_id')
        lake_name = response.meta.get('lake_name')
        records = [i for i in j['result']['values']]
        for i in records:
            item = IceoutItem()
            item['lake_id'] = lake_id
            item['lake_name'] = lake_name
            item['iceout'] = i.get('date')
            item['source'] = i.get('source')
            item['comment'] = i.get('comments')
            yield item