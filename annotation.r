#!/usr/bin/env Rscript
setwd("/home/kalea/Documents/Formation/Github/Projet_DEA")

library("RDAVIDWebService")
library(ggplot2)
library(rJava)
david<-DAVIDWebService(email="julie.solacroup@etu.u-bordeaux.fr", url="https://david.ncifcrf.gov/webservice/services/DAVIDWebService.DAVIDWebServiceHttpSoap12Endpoint/")
<<<<<<< HEAD

liste_locus<-c(read.csv("liste_locus.csv"))
genes<-liste_locus['GeneID']

genesframe<-data.frame(genes)
dim(genesframe)


result<-addList(david,genesframe,idType="ENTREZ_GENE_ID",listName="List", listType="Gene")
=======
data(demoList1)

result<-addList(david, demoList1,idType="AFFYMETRIX_3PRIME_IVT_ID",listName="demoList1", listType="Gene")
>>>>>>> f28b2d9870cab1cc21dd104b46b0f360ccf56c1a
result

# Inspect "david" object to see the gene lists selected as foreground and background.
david

selectedSpecie="Escherichia coli str. K-12 substr. MG1655"
getSpecieNames(david)
getCurrentSpeciesPosition(david)
setCurrentSpecies(david, selectedSpecie)

david
# Specifiy annotation categories.
getAllAnnotationCategoryNames(david)
setAnnotationCategories(david, c("GOTERM_BP_ALL", "GOTERM_MF_ALL", "GOTERM_CC_ALL","ENTREZ_GENE_ID","ENTREZ_GENE_SUMMARY","KEGG_PATHWAY"))

# Get functional annotation chart as R object.
FuncAnnotChart <- getFunctionalAnnotationChart(david)
FuncAnnotChart
# Print functional annotation chart to file.
getFunctionalAnnotationChartFile(david, "FuncAnnotChart.tsv")
plot2D(FuncAnnotChart,genesframe)

# Get functional annotation clustering (limited to 3000 genes).
FuncAnnotClust <- getClusterReport(david)
FuncAnnotClust
Func<-getAnnotationSummary(david)
Func

getGeneCategoriesReport(david)

# Print functional annotation clustering to file (limited to 3000 genes).
getClusterReportFile(david, "FuncAnnotClust.tsv")


#getClusterReportFile(david, type="Term",fileName="termClusterReport1.tab")

#termCluster
#head(summary(termCluster))
#clustNumber<-2
#x11()
#plot2D(termCluster,clustNumber)
#dev.print(device = png, file = "gp1.png", width = 600)