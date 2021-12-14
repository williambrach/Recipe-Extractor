import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter,IndexWriterConfig,DirectoryReader,IndexReader
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.document import Document, Field, TextField,StringField,StoredField
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.queryparser.classic import QueryParser
import sys

def search(argv):
    directory = SimpleFSDirectory(Paths.get("recipeIndex3"))
    searcher = IndexSearcher(DirectoryReader.open(directory))

    analyzer = StandardAnalyzer()
    inputText = ""
    while inputText.lower() != "exit".lower():

        if argv == "-s":
            inputText = input("Enter your search term: ").strip()
            customQuery = 'title:"{0}"^2 OR ingrediets:"{0}"^1 OR steps:"{0}" OR cleaned_ingredients:"{0}"^3'.format(inputText)
        else:
            inputText = input("Enter your query: ").strip()
            customQuery = inputText

        query = QueryParser("title", analyzer).parse(customQuery)
        scoreDocs = searcher.search(query, 100000).scoreDocs
        print("%s total matching documents." % len(scoreDocs))
        for index,scoreDoc in enumerate(scoreDocs):
            if index > 10:
                break
            doc = searcher.doc(scoreDoc.doc)
            title = doc.get("title")
            
            score = scoreDoc.score
            url = doc.get("url")
            website = doc.get("website")
            print("[{}]\t| {:.2f} | [{}]-{} | {}".format(index, score,website, title,url))

if __name__ == '__main__':
    lucene.initVM()
    print("Lucene INIT DONE.")
    if len(sys.argv) > 1:
        startArg = sys.argv[1]
    else:
       startArg = " " 
    search(startArg)