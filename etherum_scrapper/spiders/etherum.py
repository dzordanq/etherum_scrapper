import etherum_scrapper
from etherum_scrapper.items import EtherumScrapperItem
import re
import scrapy

class EtherumSpider(scrapy.Spider):
    name = 'etherum'
    allowed_domains = ['forum.ethereum.org']
    start_urls = ['https://forum.ethereum.org/']



    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_main_page)

    def parse_main_page(self, response):
        categories_xpath = "//div[@class='Box BoxCategories']//li/a[@class='ItemLink']/@href"
        for category_url in response.selector.xpath(categories_xpath).getall():
        # for category_url in response.selector.xpath(categories_xpath).getall()[:2]:
            yield scrapy.Request(url=category_url, callback=self.parse_category)

    def parse_category(self, response):
        posts_xpath = "//td[@class='DiscussionName']//a[@class='Title']/@href"
        for post_url in response.selector.xpath(posts_xpath).getall():
            yield scrapy.Request(url=post_url, callback=self.parse_post)

        next_page_xpath = "//a[@class='Next']/@href"
        if next_page_url := response.selector.xpath(next_page_xpath).get():
            yield scrapy.Request(url=next_page_url, callback=self.parse_category)

    def parse_post(self, response):
        post_content_xpath = "//div[@class='Discussion']//div[@class='Message userContent']/text()"
        post_content = response.selector.xpath(post_content_xpath).getall()
        post_text = ''.join(post_content).strip()

        ehterum_addresses = self.__find_etherum_addresses(post_text)
        for etherum_address in ehterum_addresses:
            item = EtherumScrapperItem()
            item['etherum_address'] = etherum_address
            item['post_url'] = str(response.url)
            item['is_from_comments'] = False
            item['post_content'] = post_text
            yield item
    
        response.meta.update({"postText": post_text})
        yield from self.parse_comments(response)

    

    def parse_comments(self, response):
        comments_content_xpath = "//div[@class='CommentsWrap']//div[@class='Message userContent']//text()"
        comments_content = response.selector.xpath(comments_content_xpath).getall()
        comments_text = ''.join(comments_content).strip()
        
        ehterum_addresses = self.__find_etherum_addresses(comments_text)
        for etherum_address in ehterum_addresses:
            item = EtherumScrapperItem()
            item['etherum_address'] = etherum_address
            item['post_url'] = str(response.url)
            item['is_from_comments'] = True
            item['post_content'] = response.meta['postText']
            yield item

        next_page_xpath = "//a[@class='Next']/@href"
        if next_page_url := response.selector.xpath(next_page_xpath).get():
            yield scrapy.Request(url=next_page_url, callback=self.parse_comments, meta={'postText': response.meta['postText']})

    @staticmethod
    def __find_etherum_addresses(text):
        ehterum_addresses = re.findall(r"0x[a-fA-F0-9]{40}(?![a-fA-F0-9])", text)
        if len(ehterum_addresses) > 1:
            ehterum_addresses = list(set(ehterum_addresses))
        return ehterum_addresses



            

