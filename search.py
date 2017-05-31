#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
import json

es = Elasticsearch()

qstr = input("Procurar por: ")

op_cat = input("Filtrar por categoria? (y/n) ")

if(op_cat == 'y'):
	cat = input("Que categoria? (conto, critica, cronica, miscelanea, poesia, romance, teatro, traducao) ")
else:
	cat = ""

op_ano = input("Filtrar por ano? (y/n) ")

if(op_ano == 'y'):
	ano_1 = input("Desde o ano: ")
	ano_2 = input("Até o ano: ")
else:
	ano_1 = 1
	ano_2 = 9999


if(cat == ""):
	js = {
		"size": 20,
		"query":{
			"bool":{
				"must":{
					"match":{
						"content": qstr
					}
				},
				"filter":{
					"range":{
						"year":{
							"gte": ano_1,
							"lte": ano_2
						}
					}
				}
			}
		}
	}
else:
	js = {
		"query":{
			"bool":{
				"must":{
					"match":{
						"content": qstr
					}
				},
				"filter":[
					{
					"range":{
						"year":{
							"gte": ano_1,
							"lte": ano_2
						}
					}
					},
					{
					"term":{
						"category": cat
					}
					}
				]
			}
		}
	}



result = es.search(index='lenhador', body=js)

print("Foram encontrados %d documentos" % result['hits']['total'])

for hit in result['hits']['hits']:
	print("\n%(title)s\n%(category)s - %(year)s\nLink: %(url)s" % hit["_source"])

