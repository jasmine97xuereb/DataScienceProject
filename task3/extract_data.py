# -*- coding: utf-8 -*-

import re
import urllib.request
import csv
import os
import unicodedata
import pandas as pd
from bs4 import BeautifulSoup


path = "./data"
contact_len = 8 #default length of contact number

property_list = []
resulting_property_list = []
features_of_interest = ["locality", "property_type", "bedrooms", "size_sqm", "price_euro", "contact"] #column names

#property_type_list = ["penthouse","apartment","house of character","character house","terraced house","townhouse","farmhouse","villa","maisonette",
#                  "flat","bungalow","home","plot", "palazzo","garage", "house", "premise"]
property_type_list = ["penthouse","apartment","house of character","character house","terraced house","townhouse","farmhouse","villa","maisonette",
                  "flat","bungalow","home","palazzo","house"]

#gather data from all the files having an html extension
def GetPropertyList():
  for filename in os.listdir(path):
    if filename.endswith("html"):

      f = open(path+"/"+filename, "r", encoding = 'utf-8')
      soup = BeautifulSoup(f, 'html.parser')
      
      classified_list = soup.find_all('ul', class_='classified_list')

      for c in classified_list :
        listings = c.find_all('li')
      
        for p in listings:
          data = p.find('p').get_text()
          data = data.replace("\n", "")
          data = data.replace("Property For Sale", "")
          
          #first entry is always of the following form, thus it must be ignored
          #100% FOCUSED on quality properties. Excel Homes Real Estate Ltd. www.excel.com.mt Phone 9945 1255/2141 3355.</p>
          if "100% FOCUSED" not in data:
            property_list.append(data)

      f.close()      
      #print("filename closed")

#loop through all the propreties to extract the features-of-interest
def ExtractData():
  for p in property_list:
    
    #get locality
    try:
        locality = (p.split("."))[0]
    except Exception as exception:
      locality = None

    p = p.lower()
    
    #search for a contact number and make sure it has 9 digits, else set it to none
    try:
      contact_match = re.search(r'phone[0-9\w ]*', p)
      contact_str = contact_match.group()
      contact_str = contact_str.replace(" ", "")
      contact_str = re.split('(\d+)', contact_str)[1]
      
      if(len(contact_str) != contact_len):
        contact = None
      else: 
        contact = int(contact_str)
    
    except Exception as exception:
      contact = None

    #get number of bedrooms
    try:
      #we may have either 'three bedroom' or 'three double bedroom'
      bed_match = re.search(r'[a-zA-Z1-9]*[\s\-]?[a-zA-Z1-9]*[\s\-]?[Bb]ed', p)
      bed_str = bed_match.group()
      #bed_str = bed_str.lower()
      if any (s in bed_str for s in ["one","1"]):
        bed = 1
      elif any (s in bed_str for s in ["two","2"]):
        bed = 2
      elif any (s in bed_str for s in ["three","3"]):
        bed = 3
      elif any (s in bed_str for s in ["four","4"]):
        bed = 4
      elif any (s in bed_str for s in ["five","5"]):
        bed = 5
      elif any (s in bed_str for s in ["six","6"]):
        bed = 6
      elif any (s in bed_str for s in ["seven","7"]):
        bed = 7
      elif any (s in bed_str for s in ["eight","8"]):
        bed = 8
      elif any (s in bed_str for s in ["nine","9"]):
        bed = 9
      else:
        bed = None

    except Exception as exception:
      bed = None

    #get type of property for sale
    property_type = None
    for t in property_type_list :
      if t in p:
        property_type = t
        break  #stop upon first match 

    #get property price
    try:
      price_match = re.search(r'€[\s\-]*[0-9,.]*', p)
      price_str = price_match.group()
      price = int(re.sub('[€.,\s]*', "", price_str))
    except Exception as exception:
      price = None

    #get property size
    try:
      size_match = re.search(r'[0-9]+[0-9., ]*[\s]*sqm', p)
      size_str = size_match.group()
      size_str = size_str.replace(" ","")
      size_str = size_str.replace("sqm", "")
      size = int(size_str)
    except Exception as exception:
      size = None 

    listing = [locality, property_type, bed, size, price, contact]
    resulting_property_list.append(listing)
    #print("listing list added")
  
def CreateCsv():
  data = pd.DataFrame(resulting_property_list, columns = features_of_interest)
  data.to_csv("full_property_data.csv", index = False)
  
GetPropertyList()
ExtractData()
CreateCsv()
