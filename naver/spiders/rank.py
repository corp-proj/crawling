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
text_set = []
new_text_set = []
image_set = []
title_set = []
p = 0
a = 0

class rank(scrapy.Spider):
    name = "cr"
    allowed_domains = ["naver.com"]
    start_urls = [
        "https://www.naver.com"
    ]

    def start_requests(self):
        yield scrapy.Request(f'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={self.keyword}',callback=self.parse_page_url, dont_filter=True)

    def parse_page_url(self, response):
        for i in range (1,500):
            a = '//*[@id="sp_nws'+str(i)+'"]'
            if response.xpath(a+'/div[1]/div/div[1]/div[2]/a[2]/@href').extract() != []:
                url = response.xpath(a+'/div[1]/div/div[1]/div[2]/a[2]/@href').extract()
                url_set1.append(url[0])
                if len(url_set1)==7:
                    break
        j = 7
        for o in url_set1:
            yield scrapy.Request(o, callback=self.get_url, dont_filter=True, priority=j)
            j -= 1

    def get_url(self, response):
        l = 7
        global a
        url = url_set1[a]
        a = a+1
        yield scrapy.Request(url, callback=self.parse_page_text, dont_filter=True,priority=l)
        l = l-1

    def parse_page_text(self, response):
        item = NaverItem()
        if response.xpath('//*[@id="articleBodyContents"]/text()').extract() != []:
            text=response.xpath('//*[@id="articleBodyContents"]/text()').extract()
            text_set.append(text)
            title = response.xpath('//*[@id="articleTitle"]/text()').extract()
            for t in title:
                title_set.append(t)
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
            else:
                image_set.append('None')
        elif response.xpath('//*[@id="articeBody"]/text()').extract() != []:
            text=response.xpath('//*[@id="articeBody"]/text()').extract()
            text_set.append(text)
            title = response.xpath('//*[@id="content"]/div[1]/div/h2/text()').extract()
            for t in title:
                title_set.append(t)
            image=response.xpath('//*[@id="img1"]/@src').extract()
            for y in image:
                image_set.append(y)
        elif response.xpath('//*[@id="newsEndContents"]/text()').extract() != []:
            text=response.xpath('//*[@id="newsEndContents"]/text()').extract()
            text_set.append(text)
            title = response.xpath('//*[@id="content"]/div/div[1]/div/div[1]/h4/text()').extract()
            for t in title:
                title_set.append(t)
            image = response.xpath('//*[@id="newsEndContents"]/span/img/@src').extract()
            for y in image:
                image_set.append(y)

        global p
        item['url']=url_set1[p]
        item['title']=title_set[p]
        new_text = ''
        for l in range(len(text_set[p])):
            if "\n" in text_set[p][l]:
                pass
            else:
                text_set[p][l] = re.sub('\t','',text_set[p][l])
                new_text = new_text + ' '+ text_set[p][l]
        item['text']=new_text
        item['img_url']=image_set[p]
        p += 1
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
