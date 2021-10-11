# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class RecipelinkextractorPipeline:
    def process_item(self, item, spider):

        if item['recipe_url'] in item['link']:
            csv_path = item['csv_path']
            dir_path = item['dir_path']
            # OPEN CSV FILE
            # append new line 

            # CREATE HTML FILE
            # and save it to special directory for that files 
        else:
            pass

        #return item
