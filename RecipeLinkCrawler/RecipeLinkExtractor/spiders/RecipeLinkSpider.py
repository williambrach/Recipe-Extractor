import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from ..items import RecipelinkextractorItem
import re


class RecipeLinkSpider(scrapy.Spider):
    name = "RecipeLinks"

    allowed_domains = ["bbc.co.uk"]
    handle_httpstatus_list = [404]
    recipe_url = "www.bbc.co.uk/food/recipes/"
    start_urls = ["https://www.bbc.co.uk/food"]
    csv_path = "./DATA/bbc_food.csv"
    dir_path = "./DATA/"

    visited = list()
    queue = list()
    
    
    def start_requests(self):
        for url in self.start_urls:
            self.visited.append(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if response.status != 200:
            if len(self.queue) > 0:
                link = self.queue.pop(0)
                self.visited.append(link)
                print(link)            
                yield scrapy.Request(url=link, callback=self.parse,dont_filter = True)

        item = RecipelinkextractorItem()

        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        for link in links:
            if link.nofollow == True:
                continue
            new_link = link.url.strip().strip("/") 
            if "https://www.bbc.co.uk/food/".upper() in new_link.upper() and new_link not in self.visited and new_link not in self.queue:
                self.queue.append(new_link)

        self.queue = list(set(self.queue))

        if self.recipe_url.upper() in response.request.url.upper():
            title_pattern = "<title.*?>(.+?)</title>"
            title = re.findall(title_pattern, response.text)[0]
            item['title'] = title
            item['csv_path'] = self.csv_path
            item['dir_path'] = self.dir_path
            item['links'] = links
            item['content'] = response.text
            item['url'] = response.request.url       
            yield item


        if len(self.queue) > 0:
            next_link = self.queue.pop(0)
            self.visited.append(next_link)
            print(link)       
            yield scrapy.Request(url=next_link, callback=self.parse,dont_filter = True)