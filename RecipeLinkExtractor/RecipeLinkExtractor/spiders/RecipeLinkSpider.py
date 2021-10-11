import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from ..items import RecipelinkextractorItem

class RecipeLinkSpider(scrapy.Spider):
    name = "RecipeLinks"

    allowed_domains = "bbc.food.com"
    recipe_url = ""
    start_urls = ["https://www.data-blogger.com/"]
    visited = list()
    queue = list()
    
    
    def start_requests(self):
        for url in self.start_urls:
            self.visited.append(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # The list of items that are found on the particular page
        items = []
        # Only extract canonicalized and unique links (with respect to the current page)
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        
        links  = [link for link in links if self.allowed_domains in link and (link not in self.visited or link not in self.queue)]

        # TODO extract from RESPONSE - URL, Content, Title

        self.queue.extend(links)

        if len(links) > 0:
            link = links.pop(0)
            self.visited.append(link)

            # TODO yield next step and this page to process down in pipeline 

            yield scrapy.Request(url=link, callback=self.parse)