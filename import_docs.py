#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
import json
import os

es = Elasticsearch()

print("Importing documents...")
for dirname in os.listdir(os.getcwd()+"/Obras"):
    path = os.getcwd()+"/Obras/"+dirname
    for filename in os.listdir(path):
        print(filename)
        file = open(path+"/"+filename , 'r', encoding="cp1252")
        line = file.readline()
        result = line.split(",")
        cat = result[0]
        ano = result[-1]
        if "-" in ano:
            ano = ano.split("-")[0]
        name = ""
        for i in range(1,len(result)-1):
            if i == 1:                
                name += result[i]    
            else:
                name += "," + result[i]
        print(name)
        print(cat)
        print(ano)
        jbody = {
        	"title": name,
        	"year": int(ano),
        	"category": cat,
        	"url": "http://machado.mec.gov.br/images/stories/pdf/"+dirname+"/"+filename.split(".")[0]+".pdf",
        	"content": file.read()
        }
        es.index(index='lenhador', doc_type='obras', body=jbody)

print("Import done.")