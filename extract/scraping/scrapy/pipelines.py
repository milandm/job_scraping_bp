import pymongo
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
import logging
from extract.scraping.scrapy.spiders.custom_site_spider import CustomSiteSpider
# from itemadapter import ItemAdapter

# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

import asyncio
import traceback
from log.log_config import get_logger

class DataPipeline(object):

    def __init__(self):
        self.my_logger = get_logger("DataPipeline")
        settings = get_project_settings()
        # connection = pymongo.MongoClient(
        #     settings['MONGODB_SERVER'],
        #     settings['MONGODB_PORT']
        # )
        # db = connection[settings['MONGODB_DB']]
        # self.collection = db[settings['MONGODB_COLLECTION']]

    async def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                self.my_logger.debug("Missing " + str(item))
                raise DropItem("Missing {0}!".format(data))
        self.my_logger.debug("valid "+ str(valid) + " " + str(item))
        if valid:
            # event_loop = asyncio.get_event_loop()
            # s3_bucket_put_task = loop.create_task(self.s3_bucket.put(item['page_url'], data=item['page_content']))
            # asyncio.ensure_future(await s3_bucket_put_task)
            # asyncio.run_coroutine_threadsafe(await spider.scraping_engine_object.store_scraped_content_callback(dict(item)), loop=event_loop)
            spider.scraping_engine_object.store_scraped_content_callback(dict(item))
        return item

    def close_spider(self, spider, reason):
        self.my_logger.debug(str(reason))
