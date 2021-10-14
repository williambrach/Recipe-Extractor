import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from ..items import RecipelinkextractorItem

class RecipeLinkSpider(scrapy.Spider):
    name = "RecipeLinks"

    allowed_domains = ["bbc.co.uk"]
    
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
        if response.status == 302:
            if len(self.queue) > 0:
                link = self.queue.pop(0)
                self.visited.append(link)
                print(link)            
                yield scrapy.Request(url=link, meta = {
                    'dont_redirect': True,
                    'handle_httpstatus_list': [302]}, callback=self.parse)

        item = RecipelinkextractorItem()

        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        cleanedLinks = []
        for link in links:
            if link.nofollow == True:
                continue
            link = link.url.strip().strip("/") 
            if link in self.visited:
                continue
            if "https://www.bbc.co.uk/food/".upper() in link.upper():
                cleanedLinks.append(link)
        links = cleanedLinks
        
        if self.recipe_url.upper() in response.request.url.upper():
            item['title'] = response.css("title::text")[0].get()
            item['csv_path'] = self.csv_path
            item['dir_path'] = self.dir_path
            item['links'] = links
            item['content'] = response.text
            item['url'] = response.request.url       
            yield item

        self.queue.extend(links)

        if len(links) > 0:
            link = self.queue.pop(0)
            self.visited.append(link)
            print(link)            
            yield scrapy.Request(url=link, meta = {
                  'dont_redirect': True,
                  'handle_httpstatus_list': [302]}, callback=self.parse)