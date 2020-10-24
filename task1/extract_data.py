# -*- coding: ISO-8859-1 -*-

from xml.etree.ElementTree import iterparse, XMLParser
import htmlentitydefs
import csv

author_list = [] #author_id,name
title_list = [] #title_id,title
relationship_list = [] #author_id,title_id

class CustomEntity:
    def __getitem__(self, key):
      try:
        u = unichr(htmlentitydefs.name2codepoint[key])
      except Exception as e:
        print("error encoding")
        print(e)
        exit(0)
      return u #map HTML entity names to the Unicode code points and return a string encoded using utf-8 
      #return unichr(htmlentitydefs.name2codepoint[key]).encode('utf-8') #map HTML entity names to the Unicode code points and return a string encoded using utf-8 
    
def scrape(file):
  try:
    parser = XMLParser(encoding = 'ISO-8859-1')
    parser.parser.UseForeignDTD(True)
    parser.entity = CustomEntity()

    new_article = 0
    current_title = ""
    counter = 0
    for (event, elem) in iterparse('dblp.xml', events=['start'], parser=parser):
      #if(counter < 2000000):   #251945     
      counter = counter+1
      
      if(elem.tag == 'article'):
        new_article = 1
        current_authors = []
      elif(elem.tag == 'ee'):
        new_article = 0

      if(new_article == 1):
        if(elem.tag == 'title'):
          current_title = elem.text
          
          if isinstance(current_title, unicode):
            current_title = current_title.encode('ISO-8859-1', 'ignore')
          title_list.append([current_title,"Title"])
          for author_name in current_authors:
            relationship_list.append([author_name, current_title, "PUBLISH"])

        if(elem.tag == 'author'):
          author_name = elem.text
          if isinstance(author_name, unicode):
            author_name = author_name.encode('ISO-8859-1', 'ignore')
          current_authors.append(author_name)
          #if(author_name not in author_list):
          author_list.append([author_name,"Author"])
            
      elem.clear()    
      print(counter)
      #else:
      #  break
    print("file parsed")
    
  except Exception as e:
    print("Cannot parse file")
    createCsv(["name:ID",":LABEL"], "Author.csv")
    createCsv(["title:ID",":LABEL"], "Article.csv")
    createCsv([":START_ID",":END_ID",":TYPE"], "Publish.csv")

    print("done finding - starting to write to csv ")

    writeCSV(author_list, "Author.csv")
    writeCSV(title_list, "Article.csv")
    writeCSV(relationship_list, "Publish.csv")

  #  print(e)
  #  exit(0)

def createCsv(header,filename):
  with open(filename,'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(header)
  csvFile.close()

def writeCSV(result, filename):
  with open(filename,"a") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(result)

scrape('dblp.xml')
createCsv(["name",":LABEL"], "Author.csv")
createCsv(["title",":LABEL"], "Article.csv")
createCsv([":START_ID",":END_ID","TYPE"], "Publish.csv")

print("done finding - starting to write to csv ")

writeCSV(author_list, "Author.csv")
writeCSV(title_list, "Article.csv")
writeCSV(relationship_list, "Publish.csv")
