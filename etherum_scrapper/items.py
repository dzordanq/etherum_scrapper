# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class EtherumScrapperItem(Item):
    etherum_address = Field()
    post_url = Field()
    is_from_comments = Field()
    post_content = Field()
