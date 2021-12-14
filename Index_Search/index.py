import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter,IndexWriterConfig,DirectoryReader
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.document import Document, Field, TextField,StringField,StoredField
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.queryparser.classic import QueryParser

from csv import reader
import re


def index():
    print("STARTING INDEXING.")
    store = SimpleFSDirectory(Paths.get("recipeIndex3"))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)
    count = 0
    with open('/tmp/data/spark_data_output_all.csv', 'r',encoding='utf-8') as read_obj:
        csv_reader = reader(read_obj, delimiter="\t")
        header = next(csv_reader)
        if header != None:
            for row in csv_reader:
                # storefield
                url = row[0]
                # store field
                website = row[1]
                # StringField
                title = row[2]
                # store
                servings = row[3]
                # TextField
                ingrediets = row[4][1:-1]
                # TextField
                steps = row[5][1:-1]
                # TextField
                cleaned_ingredients = row[6][1:-1]
                # TextField
                all_text = title + " " + ingrediets + " " + steps
                doc = Document()
                doc.add(Field("url", url, StoredField.TYPE))
                doc.add(Field("website", website, TextField.TYPE_STORED))
                doc.add(Field("title", title, TextField.TYPE_STORED))
                doc.add(Field("servings", servings, StoredField.TYPE))
                doc.add(Field("ingrediets", ingrediets, TextField.TYPE_STORED))
                doc.add(Field("steps", steps, TextField.TYPE_STORED))
                doc.add(Field("cleaned_ingredients", cleaned_ingredients, TextField.TYPE_STORED))
                doc.add(Field("alltext", all_text, TextField.TYPE_STORED))
                writer.addDocument(doc)
                count += 1
    print(count)
    writer.commit()
    writer.close()
    print("INDEXING DONE.")

if __name__ == '__main__':
    lucene.initVM()
    print("Lucene INIT DONE.")
    index()

 #(title:"souffle"^2 OR ingrediets:"souffle"^1 OR steps:"souffle" OR cleaned_ingredients:"souffle"^3) AND website:"spoon"

