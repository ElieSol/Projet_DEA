# -*- coding: utf-8 -*

import sys
import re
import os
import csv


#
# Part where the RegulonDB files are parsed to extract the Gene ID and the corresponding locus
#

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
    print el["GeneID"]

#
# Part to save the list of dictionary in a csv file
#

csv_columns = ['Locus', 'GeneID']
csv_file = "liste_locus.csv"

try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in list_locus:
            writer.writerow(data)
except IOError:
    print("I/O error") 

# 
# Part to execute the R script which contain the annotation service (RDavidWebService)
#

os.system("RScript annotation.R")

