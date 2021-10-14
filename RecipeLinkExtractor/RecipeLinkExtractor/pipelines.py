import csv
import os

from itemadapter import ItemAdapter


class RecipelinkextractorPipeline:
    
    def process_item(self, item, spider):

        path_to_file = item['dir_path'] + "/" + item['title']+".html"
        # check if csv file exists
        if not os.path.isfile(item['csv_path']):
            print(item['csv_path'])
            with open(item['csv_path'], 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f, delimiter='\t')
                writer.writerow(["title", "url", "path_to_file"])
                f.close()
        # # add new row into dataset
        with open(item['csv_path'], 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f, delimiter='\t')
            # write the data
            writer.writerow([item['title'],item['url'],path_to_file])
            f.close()

        # save html file
        file = open(path_to_file,"w", encoding='UTF8')
        file.write(item['content'])
        file.close()

        return item
