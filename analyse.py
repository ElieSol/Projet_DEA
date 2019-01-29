# -*- coding: utf-8 -*

import sys
import re

file_GeneProduct = open("File_Regulon_DB/GeneProductSet.txt","r")
file_Condition = open("File_Regulon_DB/GCSet.txt","r")

products = file_GeneProduct.readline()
condition = file_Condition.readline()

dict = {}
list_locus = []
locus = r"(^ECK)"
cpt = 0
result=[]
for line in file_GeneProduct:
    if line[0]!="#":
        dict = {}
        a = re.search(r"\ECK12\w+", line)
        b =  re.search(r"", line)       
        locus = a.group()
        dict["Locus"]=locus
        geneID = line.split("	")[1]
        dict["GeneID"]=geneID
        list_locus.append(dict)
        cpt+=1



print cpt

for el in list_locus:
    print el


