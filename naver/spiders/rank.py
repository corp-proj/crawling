import scrapy
import asyncio
import time
from naver.items import NaverItem
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
from scrapy.signalmanager import dispatcher
import re

rank_set = ['1','2','3','4','5','6','7','8','9','10']
key_set = []
url_set1 = []
url_set2 = []
text_set = []
new_text_set = []
image_set = []
related_set = []
i = 0
a = 0

class rank(scrapy.Spider):
    name = "cr"
    allowed_domains = ["rank.ezme.net","naver.com"]
    start_urls = [
        "http://rank.ezme.net/"
    ]


    def parse(self, response): 
        item = NaverItem()
        for sel in response.xpath('/html/body/div[1]/main/div/div[3]/div/div/h4/a'):
            key = sel.xpath('./b/text()').extract()
            for s in key:
                key_set.append(s)
        k = 10
        for i in range(1,11):
            for l in range(1,4):
                related = response.xpath('/html/body/div[1]/main/div/div[3]/div['+str(i)+']/div/h4/div['+str(l)+']/a/span/text()').extract()
                if related == []:
                    related = ['None']
                for p in related:
                    related_set.append(p)
        for i in range(10):
            url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query="+key_set[i]
            url_set1.append(url)
            yield scrapy.Request(url, callback=self.parse_page_url, dont_filter=True,priority=k)
            k = k-1

    
    def parse_page_url(self, response):
        item = NaverItem()
        for i in range (1,100):
            a = '//*[@id="sp_nws'+str(i)+'"]'
            if response.xpath(a+'/div[1]/div/div[1]/div/a[2]/@href').extract() != []:
                url = response.xpath(a+'/div[1]/div/div[1]/div/a[2]/@href').extract()
                break
        for i in url:
            url_set2.append(i)
            yield scrapy.Request(i, callback=self.get_url, dont_filter=True)
        
    def get_url(self, response):
        l = 10
        global a
        url = url_set2[a]
        a = a+1
        yield scrapy.Request(url, callback=self.parse_page_text, dont_filter=True,priority=l)
        l = l-1

    def parse_page_text(self, response):
        item = NaverItem()
        if response.xpath('//*[@id="articleBodyContents"]/text()').extract() != []:
            text=response.xpath('//*[@id="articleBodyContents"]/text()').extract()
            if response.xpath('//*[@id="articleBodyContents"]/span[1]/img/@src').extract() != []:
                image=response.xpath('//*[@id="articleBodyContents"]/span[1]/img/@src').extract()
                for y in image:
                    image_set.append(y)
            elif response.xpath('//*[@id="articleBodyContents"]/table/tbody/tr/td/table/tbody/tr[1]/td/span/img/@src').extract() != []:
                image=response.xpath('//*[@id="articleBodyContents"]/table/tbody/tr/td/table/tbody/tr[1]/td/span/img/@src').extract()
                for y in image:
                    image_set.append(y)                
            text_set.append(text)
        elif response.xpath('//*[@id="articeBody"]/text()').extract() != []:
            text=response.xpath('//*[@id="articeBody"]/text()').extract()
            image=response.xpath('//*[@id="img1"]/@src').extract()
            text_set.append(text)
            for y in image:
                image_set.append(y)
        elif response.xpath('//*[@id="newsEndContents"]/text()').extract() != []:
            text=response.xpath('//*[@id="newsEndContents"]/text()').extract()
            image = response.xpath('//*[@id="newsEndContents"]/span/img/@src').extract()
            text_set.append(text)
            for y in image:
                image_set.append(y)
        
        item = NaverItem()
        global i
        item['rank']=rank_set[i]
        item['key']=key_set[i]
        item['url']=url_set2[i]
        related_get = []
        related_get.append(related_set[3*i])
        related_get.append(related_set[(3*i)+1])
        related_get.append(related_set[(3*i)+2])
        item['related'] = related_get
        new_text = ''
        for l in range(len(text_set[i])):
            if "\n" in text_set[i][l]:
                pass
            else:
                text_set[i][l] = re.sub('\t','',text_set[i][l])
                new_text = new_text + ' '+ text_set[i][l]
        item['text']=new_text
        item['img_url']=image_set[i]
        i = i+1
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

