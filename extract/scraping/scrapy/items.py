# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebPageItem(scrapy.Item):
    company_domain = scrapy.Field()
    page_url = scrapy.Field()
    page_content = scrapy.Field()

    def __repr__(self):
        return repr({"page_url": self["page_url"]})
