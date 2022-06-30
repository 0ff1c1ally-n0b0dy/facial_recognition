#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests 
import json 
import pandas as pd
import time
import urllib
import urllib.request 
from urllib.error import HTTPError
from bs4 import *
import os
import unidecode

save_dir=r"C:\Users\mihnea.andrei\Python scripts\resnet_andrei\wiki_face_parser\images"

def timming(since):
    now=time.time() 
    s=now-since
    m=int(s/60)
    s=s-m*60
    return "%dm %ds"%(m,s)


# In[ ]:


count_links=464800
count_people=0
start=time.time()
printing_iter=10**(2)
file1=open(r"C:\Users\mihnea.andrei\Python scripts\resnet_andrei\wiki_face_parser\names\Print_details.txt","w")
print_data=""
image_name=""

while True:
    prefix="Q"+str(count_links)
    flag=1
    wiki_link="https://www.wikidata.org/wiki/%s"%(prefix)
    json_link="https://www.wikidata.org/wiki/Special:EntityData/%s.json"%(prefix) 
    try:
        response=requests.get(json_link)
    except requests.exceptions.Timeout:
        print("Too much time to request wikipedia link %s"%(image_link))
        flag=0
    except requests.exceptions.TooManyRedirects:
        print("Bad wikipedia link %s"%(image_link))
        flag=0
    except requests.exceptions.RequestException as e:
        print("Catastrophic error for wikipaedia link %s"%(image_link))
        flag=0
    if flag==1:
        try: 
            person=json.loads(response.content)
        except ValueError as err:
            flag=0
    if flag==1:
        if prefix in person["entities"].keys(): 
            if "P31" in person["entities"][prefix]["claims"].keys():
                if "mainsnak" in person["entities"][prefix]["claims"]["P31"][0].keys():
                    if "datavalue" in person["entities"][prefix]["claims"]["P31"][0]["mainsnak"].keys():
                        if "value" in person["entities"][prefix]["claims"]["P31"][0]["mainsnak"]["datavalue"].keys():
                            if "id" in person["entities"][prefix]["claims"]["P31"][0]["mainsnak"]["datavalue"]["value"].keys():
                                if person["entities"][prefix]["claims"]["P31"][0]["mainsnak"]["datavalue"]["value"]["id"]=="Q5":
                                    #############3
                                    #Obtain the name
                                    ##############3
                                    person_name=""
                                    if "entities" in person.keys():   
                                        if prefix in person["entities"].keys():
                                            if "labels" in person["entities"][prefix].keys(): 
                                                if "en" in person["entities"][prefix]["labels"].keys():
                                                    person_name=person["entities"][prefix]["labels"]["en"]["value"]
                                                    #remove quotes since it gives an error when the image file name when saved
                                                    if '"' in person_name:
                                                        person_name=person_name.replace('"',"")
                                                    if "/" in person_name:
                                                        person_name=person_name.replace('/',"")
                                                    if " "in person_name:
                                                        person_name=person_name.replace(' ',"")
                                                    if "\\" in person_name:
                                                        person_name=person_name.replace(' ',"")
                                                    if "." in person_name:
                                                        person_name=person_name.replace('.',"")
                                                    if "?" in person_name:
                                                        person_name=person_name.replace("?","")
                                                    if "!" in person_name:
                                                        person_name=person_name.replace("!","")
                                                    #remove accents, diacritics
                                                    person_name=unidecode.unidecode(person_name)
                                    ##########
                                    #Obtain the image
                                    #########
                                    if person_name!="":
                                        if "claims" in person["entities"][prefix].keys():
                                            if "P18" in person["entities"][prefix]["claims"].keys():
                                                if "mainsnak" in person["entities"][prefix]["claims"]["P18"][0].keys():
                                                    if "datavalue" in person["entities"][prefix]["claims"]["P18"][0]["mainsnak"].keys():
                                                        if "value" in person["entities"][prefix]["claims"]["P18"][0]["mainsnak"]["datavalue"].keys():
                                                            image_name=person["entities"][prefix]["claims"]["P18"][0]["mainsnak"]["datavalue"]["value"]
                                                            if '"' in image_name:
                                                                image_name=image_name.replace('"','')
                                                            if "\\" in image_name:
                                                                image_name=image_name.replace("\\","")
                                                            image_suffix="_".join(image_name.split(" "))
                                                            image_link="https://www.wikidata.org/wiki/%s#/media/File:%s"%(prefix,image_suffix)
                                                            #image_link = urllib.parse.quote(link,safe=':/')
                                                            try:
                                                                r=requests.get(image_link)
                                                            except requests.exceptions.Timeout:
                                                                print("Too much time to request image link %s"%(image_link))
                                                                flag=0
                                                            except requests.exceptions.TooManyRedirects:
                                                                print("Bad image link %s"%(image_link))
                                                                flag=0
                                                            except requests.exceptions.RequestException as e:
                                                                print("Catastrophic error for image link %s"%(image_link))
                                                                flag=0
                                                            if flag==1:
                                                                #parse HTML code
                                                                soup=BeautifulSoup(r.text,"html.parser")
                                                                #find all images in url (should only be 1 here)
                                                                images=soup.findAll('img')
                                                                if len(images)!=0:
                                                                    image=images[0]
                                                                    try:
                                                                        image_link=image["src"]
                                                                    except:
                                                                        flag=0
                                                                    if flag==1:
                                                                        image_link="https:"+image_link
                                                                        try:
                                                                            urllib.request.urlretrieve(image_link,save_dir+"\\"+person_name+".jpg")
                                                                        except Exception as e:
                                                                            print("%s for image has error %s, link:%s"%(image_name,e,image_link))
                                                                            flag=0
                                                                        if flag==1:
                                                                            #print("Success for %s with link %s"%(image_name,image_link))
                                                                            count_people+=1
                                                        
    count_links+=1
    if count_links%printing_iter==0:
        try:
            print("Downloaded %d images \t Tried %d links \t Last person: %s \t %s time"%(count_people,count_links,person_name,timming(start)))
        except NameError:
            pass
     


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




