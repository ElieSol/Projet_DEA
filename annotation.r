#!/usr/bin/env Rscript


testFunction <- function(){
    print('This is a test')
}

#read.csv2(”liste_locus.csv”,header=TRUE)
#print(readLines(”liste_locus.csv”))
library("RDAVIDWebService")
library(ggplot2)
david<-DAVIDWebService(email="julie.solacroup@etu.u-bordeaux.fr", url="https://david.ncifcrf.gov/webservice/services/DAVIDWebService.DAVIDWebServiceHttpSoap12Endpoint/")
data(demoList1)
result<-addList(david, demoList1,idType="AFFYMETRIX_3PRIME_IVT_ID",listName="demoList1", listType="Gene")
result
setAnnotationCategories(david, c("GOTERM_BP_ALL","GOTERM_MF_ALL", "GOTERM_CC_ALL"))
termCluster<-getClusterReport(david, type="Term")
getClusterReportFile(david, type="Term",fileName="termClusterReport1.tab")

termCluster
head(summary(termCluster))
clustNumber<-2
plot2D(termCluster,clustNumber)

testFunction()
