# -*- coding: utf-8 -*

import sys
import re
import os
import csv


#
# Part where the RegulonDB files are parsed to extract the Gene ID, Gene Product and the corresponding locus
#
# It uses the list_locus.txt generated in the tulip script i.e. the file scriptFonctionnel.py
#


file_GeneProduct = open("File_Regulon_DB/GeneProductSet.txt","r")
file_Cluster = open("list_locus.txt","r")

products = file_GeneProduct.readline()
cluster = file_Cluster.readline()

list_locus_cluster = []
nb_l = 0
for line in file_Cluster:
    line = line.strip('\n')
    list_locus_cluster.append(str(line))
    nb_l+=1

dict = {}
list_locus = []
locus = r"(^ECK)"
cpt = 0
result=[]
for line in file_GeneProduct:
    if line[0]!="#":
        a = re.search(r"\ECK12\w+", line)
        b =  re.search(r"", line)
        locus = a.group()
        if str(locus) in list_locus_cluster:
            dict = {}       
            dict["Locus"]=locus
            geneID = line.split("	")[1]
            if((len(line.split("	"))>6)):
                product=line.split("	")[6]
            else:
                product=""
            dict["GeneID"]=geneID
            dict["Product"]=product
            list_locus.append(dict)
            cpt+=1

#
# Part to save the list of dictionary in a csv file
#

csv_columns = ['Locus', 'GeneID','Product']
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
# Note: not working
#
os.system("Rscript annotation.r")

