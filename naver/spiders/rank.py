import scrapy
import asyncio
import time
from naver.items import NaverItem
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
from scrapy.signalmanager import dispatcher
import re

key_set = []
url_set1 = []
url_set2 = []
text_set = []
new_text_set = []
image_set = []

class rank(scrapy.Spider):
    name = "cr"
    allowed_domains = ["naver.com"]
    start_urls = [
        "https://www.naver.com"
    ]

    def start_requests(self):
        yield scrapy.Request(f'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={self.keyword}',callback=self.parse_page_url, dont_filter=True)

    def parse_page_url(self, response):
        for i in range (1,100):
            a = '//*[@id="sp_nws'+str(i)+'"]'
            if response.xpath(a+'/div[1]/div/div[1]/div/a[2]/@href').extract() != []:
                url = response.xpath(a+'/div[1]/div/div[1]/div/a[2]/@href').extract()
                break
        for i in url:
            url_set2.append(i)
            yield scrapy.Request(i, callback=self.get_url, dont_filter=True)
        
    def get_url(self, response):
        url = url_set2[0]
        yield scrapy.Request(url, callback=self.parse_page_text, dont_filter=True)

    def parse_page_text(self, response):
        item = NaverItem()
        if response.xpath('//*[@id="articleBodyContents"]/text()').extract() != []:
            text=response.xpath('//*[@id="articleBodyContents"]/text()').extract()
            text_set.append(text)
            if response.xpath('//*[@id="articleBodyContents"]/span[1]/img/@src').extract() != []:
                image=response.xpath('//*[@id="articleBodyContents"]/span[1]/img/@src').extract()
                for y in image:
                    image_set.append(y)
            elif response.xpath('//*[@id="articleBodyContents"]/div/div/span[1]/img/@src').extract() != []:
                image=response.xpath('//*[@id="articleBodyContents"]/div/div/span[1]/img/@src').extract()
                for y in image:
                    image_set.append(y)
            elif response.xpath('//*[@id="articleBodyContents"]/table/tbody/tr/td/table/tbody/tr[1]/td/span/img/@src').extract() != []:
                image=response.xpath('//*[@id="articleBodyContents"]/table/tbody/tr/td/table/tbody/tr[1]/td/span/img/@src').extract()
                for y in image:
                    image_set.append(y)                
        elif response.xpath('//*[@id="articeBody"]/text()').extract() != []:
            text=response.xpath('//*[@id="articeBody"]/text()').extract()
            text_set.append(text)
            image=response.xpath('//*[@id="img1"]/@src').extract()
            for y in image:
                image_set.append(y)
        elif response.xpath('//*[@id="newsEndContents"]/text()').extract() != []:
            text=response.xpath('//*[@id="newsEndContents"]/text()').extract()
            text_set.append(text)
            image = response.xpath('//*[@id="newsEndContents"]/span/img/@src').extract()
            for y in image:
                image_set.append(y)


        item['url']=url_set2[0]
        new_text = ''
        for l in range(len(text_set[0])):
            if "\n" in text_set[0][l]:
                pass
            else:
                text_set[0][l] = re.sub('\t','',text_set[0][l])
                new_text = new_text + ' '+ text_set[0][l]
        item['text']=new_text
        item['img_url']=image_set[0]
        return item

    def spider_results():
        results = []
        
        def crawler_results(signal, sender, item, response, spider):
            results.append(item)
        
        dispatcher.connect(crawler_results, signal=signals.item_scraped)
        process = CrawlerProcess(get_project_settings())
        process.crawl(rank)
        process.start()
        return results


if __name__=='__main__':
    print(spider_results())
