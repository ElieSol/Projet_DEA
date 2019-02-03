#!/usr/bin/env Rscript

setwd("/home/kalea/Documents/Formation/Github/Projet_DEA")
library("RDAVIDWebService")
library(ggplot2)
library(rJava)
david<-DAVIDWebService(email="julie.solacroup@etu.u-bordeaux.fr", url="https://david.ncifcrf.gov/webservice/services/DAVIDWebService.DAVIDWebServiceHttpSoap12Endpoint/")

# load data
liste_locus<-c(read.csv("liste_locus.csv"))
genes<-liste_locus['GeneID']

genesframe<-data.frame(genes)
dim(genesframe)

# Add the List in the "David space"
result<-addList(david,genesframe,idType="ENTREZ_GENE_ID",listName="List", listType="Gene")
result

# Inspect "david" object to see the gene lists selected as foreground and background.
david

# Attempt to change the current species
selectedSpecie="Escherichia coli str. K-12 substr. MG1655"
getSpecieNames(david)
#setCurrentSpecies(david, selectedSpecie)

# Specifiy annotation categories.
getAllAnnotationCategoryNames(david)
setAnnotationCategories(david, c("GOTERM_BP_ALL", "GOTERM_MF_ALL", "GOTERM_CC_ALL","ENTREZ_GENE_ID","ENTREZ_GENE_SUMMARY","KEGG_PATHWAY"))

# Get functional annotation chart as R object.
FuncAnnotChart <- getFunctionalAnnotationChart(david)

# Print functional annotation chart to file.
getFunctionalAnnotationChartFile(david, "FuncAnnotChart.tsv")

# Get functional annotation clustering (limited to 3000 genes).
FuncAnnotClust <- getClusterReport(david)
Func<-getAnnotationSummary(david)
Func
getGeneCategoriesReport(david)

# Print functional annotation clustering to file (limited to 3000 genes).
getClusterReportFile(david, "FuncAnnotClust.tsv")

head(summary(FuncAnnotClust))
clustNumber<-6
x11()
plot2D(FuncAnnotClust,clustNumber)
dev.print(device = png, file = "clust.png", width = 1500)