# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from etherum_scrapper.settings import FEED_EXPORT_FIELDS
from scrapy.exporters import CsvItemExporter
import csv

class EtherumScrapperPipeline:
    def __init__(self) -> None:
        self.file_handle = open('data.csv', 'wb')
        self.__set_exporter()
       
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file_handle.close()

    def __set_exporter(self):
        self.exporter = CsvItemExporter(self.file_handle, include_headers_line=True, delimiter=",", quotechar=r"'", quoting=csv.QUOTE_ALL, fields_to_export=FEED_EXPORT_FIELDS)
        self.exporter.start_exporting()

