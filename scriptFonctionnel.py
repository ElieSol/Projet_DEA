# Powered by Python 2.7

# DEA Project
#
# Authors: 
#  - Economides Marie
#  - Solacroup Julie
#
from tulip import tlp
from collections import deque


# Variables
NODE_WIDTH = 12
NODE_HEIGHT = 4


##########
# Part 1 #
##########

# Function to display the labels on the network's nodes
# 
# Parameters: g (graph), label (viewLabel), locus
# Return: None
#
def displayLabels(g,label,locus):
  labelPosition = g.getIntegerProperty("viewLabelPosition")
  for node in g.getNodes():
    label[node] = locus[node]
    labelPosition[node]=tlp.LabelPosition.Center
  

# Function to set the nodes size
# 
# Parameters: g (graph), size (viewSize)
# Return: None
#
def setNodesSize(g,size):
  nodeSize = tlp.Size(NODE_WIDTH, NODE_HEIGHT,0)
  for node in g.getNodes():
    size[node] = nodeSize


# Function to set edges colors depending on regulation types
# - Positive Regulations are colored in green 
# - Negative Regulations are colored in red
# - Neutral Regulations are colored in violet
#
# Parameters: g (graph), color (viewColor), positive, negative
# Return: None
#
def setDisplayOfEdges(g, viewColor, positive, negative):
  for edge in g.getEdges():
    if positive[edge] == True and negative[edge] == False:
      viewColor[edge] = tlp.Color.Green
    if positive[edge] == False and negative[edge] == True:
      viewColor[edge] = tlp.Color.Red
    if positive[edge] == True and negative[edge] == True:
      viewColor[edge] = tlp.Color.Blue
    if positive[edge] == False and negative[edge] == False:
      viewColor[edge] = tlp.Color.Black
  updateVisualization()
  

# Function to set nodes' positions and graph form by using Tulips' drawing Algorithm
# 
# Parameters: g (graph), layout (viewLayout)
# Return: None
#
def setNodesPosition(g, layout):
  parameters = tlp.getDefaultPluginParameters("Circular (OGDF)")
  parameters["Unit edge length"] = 80
  g.applyLayoutAlgorithm('Circular (OGDF)', layout, parameters)
  updateVisualization()


# Function to modify the general layout of the graph  
# It allows the display of labels, the modification of the edges color, the modification of the nodes size and their position. 
#
# Parameters: graph, label (viewLabel), size (viewSize), color (viewColor), positive, negative, layout
# Return: None
#
def setGraphLayout(graph, label, locus, size, color, positive, negative, layout):
  displayLabels(graph,label,locus)
  setNodesSize(graph,size)
  setDisplayOfEdges(graph, color, positive, negative)
  setNodesPosition(graph, layout)
  


##########
# Part 2 #
##########

# Function to create a Hierarchical Tree
# 
# Parameters: tree (empty subgraph), root (node), cluster (list of subgraphs)
# Return: None
#
def createHierarchicalTree(tree,root,cluster):
  for sub_graph in cluster:
    node=tree.addNode()
    tree.addEdge(root,node)
    current_cluster=sub_graph.getSubGraphs()
    createHierarchicalTree(tree,node,current_cluster)
    if sub_graph.numberOfSubGraphs()==0:
      for n in sub_graph.getNodes():
        tree.addNode(n)
        tree.addEdge(node,n)


# Function to create a radial version of the Hierarchical Tree
# 
# Parameters: tree (Hierarchical Tree)
# Return: None
#
def getRadialTreeVersion(tree):
  params = tlp.getDefaultPluginParameters('Tree Radial', tree)
  tree.applyLayoutAlgorithm('Tree Radial', params)

  
# Function to color nodes by using values of the 'Double Property'
# 
# Parameters: graph, property, color (viewColor)
# Return: None
#
def colorNodes(g, property, color):
  heatMap = tlp.ColorScale([tlp.Color.Red, tlp.Color.Black, tlp.Color.Green])
  params = tlp.getDefaultPluginParameters('Color Mapping', g)
  params['input property']=property
  params['target']='nodes'
  params['color scale']= heatMap
  g.applyColorAlgorithm('Color Mapping', params)


# Function to create, display a radial hierarchical tree (if an other hierarchical tree exists, it will be deleted and replace by a new one)
#
# Parameters : graph (root graph), metric (viewMetric), color (viewColor)
# Return: None
#  
def displayHierarchicalTree(graph, metric, color):
  if(graph.getSubGraph("Hierarchical Tree")!=None):
  	graph.delSubGraph(graph.getSubGraph("Hierarchical Tree"))  
  
  genes_interaction= graph.getSubGraph("Genes interactions")
  cluster= genes_interaction.getSubGraphs()
  tree = graph.addSubGraph("Hierarchical Tree")
  racine = tree.addNode()
  
  createHierarchicalTree(tree,racine,cluster)
  getRadialTreeVersion(graph.getSubGraph("Hierarchical Tree"))
  colorNodes(graph.getSubGraph("Hierarchical Tree"), metric, color)
  

# Function to find the shortest path between two nodes in a graph
#
# Parameters: graph, n (node), path (list of node in the path, empty when the function is called)
# Return: List of node in the shortest path
#
def findPath(graph, n, root, path=[]):
  path+=[n]
  if(n==root):
    return path
  if graph.isElement(n)!=True:
    return None
  for neigbor in graph.getInOutNodes(n):
    findPath(graph, neigbor, root, path)
    if(neigbor == root):
      return path
    if(neigbor in path):
      return path
    if(neigbor!= root and neigbor not in path):
      findPath(graph, neigbor, root, path)
  return path  


# Utility function to remove duplicates between two list (or path) and keep the root
#
# Parameters: list_1 (first path), list_2 (second path)
# Return: list (the final path)
#
def removeDuplicate(list_1,list_2):
  match = list(set(list_1) & set(list_2))
  if len(match)<=2 and len(match)>0:
     root = match[len(match)-1]
  elif len(match)>2:
     root=match[0]
  list_2=list_2[::-1]
  for el in match:
    list_1.remove(el)
    list_2.remove(el)
  finalList = list_1 +[root]+ list_2
  return finalList


# Function to find the shortest path
#
# Parameters: graph (root graph), n1 (source node), n2 (target node)
# Return: list (the final path)
#
def findShortestPath(graph, n1, n2):
  list_node = []
  tree = graph.getSubGraph("Hierarchical Tree")
  i=0
  for n in tree.getNodes():
    list_node.append(n) 
    i+=1
  root = list_node[0]
  pathway_1=findPath(tree, n1, root, path=[])
  pathway_2=findPath(tree, n2, root, path=[])
  pathway = removeDuplicate(pathway_1,pathway_2)
  pathway.pop(0)
  pathway.pop(len(pathway)-1)
  return pathway


# Function to create the gene interactions graph with curved edge
#
# Parameters: g (root graph), gLayout (viewLayout), gShape (viewShape)
# Return: None
#
def createBundles(g, gLayout, gShape):
  for edge in g.getEdges():
    print("EDGE = ",edge)
    shortestpath=findShortestPath(g,g.source(edge), g.target(edge))
    nodesPath=[]
    for node in shortestpath:
      nodesPath.append(gLayout[node])
    gLayout.setEdgeValue(edge,nodesPath)
  gShape.setAllEdgeValue(16)


# -----------------------------------------------------------------
#
# The following lines were intended to be used, but unfortunately we couldn't make it work
#
# -----------------------------------------------------------------
# Function to find the shortest path between two nodes in a graph
#
# Parameters: graph, start (node1), end (node2), path (list of node in the path, empty when the function is called)
# Return: path (list of node in the shortest path)
# --------------------------------------------------------
#def findParent(graph,u,v,viewLevel):
#	uPath=[]
#	vPath=[]
#	uAncestor=u
#	vAncestor=v
#	while uAncestor!=vAncestor:
#		if viewLevel[uAncestor]>viewLevel[vAncestor]:
#			for uAnc in graph.getInNodes(uAncestor):
#				uPath.append(uAnc)
#				uAncestor=uAnc			
#		elif viewLevel[vAncestor]>viewLevel[vAncestor]:
#			for vAnc in graph.getInNodes(vAncestor):
#				vPath.append(vAnc)
#				vAncestor=vAnc
#		elif viewLevel[uAncestor]==viewLevel[vAncestor]:
#			for uAnc in graph.getInNodes(uAncestor):
#				uPath.append(uAnc)
#				uAncestor=uAnc
#			for vAnc in graph.getInNodes(vAncestor):
#				vPath.append(vAncestor)
#				vAncestor=vAnc			
#		else:
#			print("Almost done")
#			path=[]
#			for node in uPath:
#				if node!=uAncestor:
#					path.append(node)
#			path.append(uAncestor)
#			vPath.reverse()
#			for node in vPath:
#				if node!=uAncestor:
#					path.append(node)
#			return path
#
# ----------------------------------------------------------------
# Function to create the gene interactions graph with curved edge
#
# Parameters: tree, graph, viewLevel, gLayout (viewLayout), gShape (viewShape)
# Return: None
# --------------------------------------------------------
#		
#def createBundles(tree, graph, viewLevel,gLayout,gShape):
#	for edge in graph.getEdges():
#		u = graph.source(edge)
#		v = graph.target(edge)
#		path=findParent(tree,u,v,viewLevel)
#		nodePath=[]
#		if path!= None:
#			for node in path:
#				nodePath.append(gLayout[node])
#			gLayout.setEdgeValue(edge,nodePath)
#	gShape.setAllEdgeValue(16)		
#
# -----------------------------------------------------------------

##########
# Part 3 #
##########

 
# Function to create the small multiples graph and its subgraphs
#
# Parameters: g (graph racine), timelapse (list of tp_*)
# Return: None
# 
def createSmallMultiples(g, timelapse):
  smallMultiples = g.addSubGraph("smallMultiples")
  list_node = []
  gInteract = g.getSubGraph("Genes interactions")
  for n in gInteract.getNodes():
    list_node.append(n) 
  i=1
  for lapse in timelapse:
    name = "tp "+str(i)
    tp = smallMultiples.addSubGraph(name)
    tlp.copyToGraph(tp,gInteract)
    metricTP = tp.getDoubleProperty("viewMetric")
    for node in tp.getNodes():
      metricTP[node]= lapse[node]
    i+=1


# Function to color the small multiples graphs by geneexpression
#
# Parameters: g (graph racine), timelapse (list of tp_*), gInteractions (graph)
# Return: None
# 
def colorSmallMultiples(g,color):
  colorG = g.getColorProperty("viewColor")
  metric = g.getDoubleProperty("viewMetric")
  colorNodes(g, metric, colorG)
  for smaliImg in g.getSubGraphs():
    localproperty = smaliImg.getLocalDoubleProperty("viewMetric")
    color = smaliImg.getLocalColorProperty("viewColor")
    colorNodes(smaliImg, localproperty, color)
  


# Function to place each subgraphs of the small multiples graph in a grid according to a number of columns
#
# Parameters: g (root graph), timelapse (list of tp_*), gInteractions (genes interactions graph)
# Return: None
# 
def positionSmallMultiples(g, smallG, columnNumber):
  layout = g.getLayoutProperty("viewLayout")
  graphBoundingBox = tlp.computeBoundingBox(g)
  gHeight = graphBoundingBox.height()
  gWidth = graphBoundingBox.width()
  n = 1
  y = 0
  line=0
  for smallImg in smallG.getSubGraphs():
    if n==columnNumber+1:
      line+=1
      y=-gHeight*line*1.5
      n = 1
    x = gWidth*n*1.5
    newCenter = tlp.Vec3f(x,y,0)
    layout.center(newCenter, smallImg)
    n+=1


# Function to display the small version of each graph of each timelapse in a grid
#
# Parameters: g (graph racine), timelapse (list of tp_*), color (viewColor), numberOfColumn
# Return: None
#
def displaySmallImages(graph, timelapse, color, numberOfColumn): 
  createSmallMultiples(graph, timelapse)
  smallMult = graph.getSubGraph("smallMultiples")
  colorSmallMultiples(smallMult,color)
  positionSmallMultiples(graph, smallMult, numberOfColumn)



##########
# Part 4 #
##########

#
# Function to save each cluster and their locus in a list
# 
# Parameters: g (root graph)
# Return: List of cluster
#
def getClusters(g):
  gInteract = graph.getSubGraph("Genes interactions")
  n = 1 # Number of clusters
  clusters = []
  for subg in gInteract.getSubGraphs():
    cluster = []
    if subg.getSubGraph("unnamed")!=None:
      m = 1 # Number of sub-clusters
      subcluster = []
      cluster.append(subcluster)
      for subsub in subg.getSubGraphs():
        for node in subg.getNodes():
          dictNode={}
          dictNode['Locus']=Locus[node]
          if Positive[node]==True and Negative[node]==False:
            dictNode['Regulation']= "+"
          if Positive[node]==False and Negative[node]==True:
            dictNode['Regulation']= "-"
          else:
            dictNode['Regulation']= ""
          subcluster.append(dictNode)
      m+=1
    for node in subg.getNodes():
      dictNode={}
      dictNode['Locus']=Locus[node]
      if Positive[node]==True and Negative[node]==False:
        dictNode['Regulation']= "Positive"
      if Positive[node]==False and Negative[node]==True:
        dictNode['Regulation']= "Negative"
      else:
        dictNode['Regulation']= ""
      cluster.append(dictNode)
    clusters.append(cluster) 
    n+=1
  print(clusters)
  return clusters

#
# Function to get all locus of the Genes interaction graph and save them in a txt file
#
# Parameters : g (root graph), Locus (Locus attribute of the root graph)
# Return : None
#
def getAllLocus(g, Locus):
  list_locus = []
  for n in g.getSubGraph("Genes interactions").getNodes():
    list_locus.append(Locus[n])
  print(list_locus)
  with open('list_locus.txt','w') as f:
    for item in list_locus:
      f.write("%s\n" % item)



# MAIN #
def main(graph): 
  Locus = graph.getStringProperty("Locus")
  Negative = graph.getBooleanProperty("Negative")
  Positive = graph.getBooleanProperty("Positive")
  locus = graph.getStringProperty("locus")
  similarity = graph.getDoubleProperty("similarity")
  tp1_s = graph.getDoubleProperty("tp1 s")
  tp10_s = graph.getDoubleProperty("tp10 s")
  tp11_s = graph.getDoubleProperty("tp11 s")
  tp12_s = graph.getDoubleProperty("tp12 s")
  tp13_s = graph.getDoubleProperty("tp13 s")
  tp14_s = graph.getDoubleProperty("tp14 s")
  tp15_s = graph.getDoubleProperty("tp15 s")
  tp16_s = graph.getDoubleProperty("tp16 s")
  tp17_s = graph.getDoubleProperty("tp17 s")
  tp2_s = graph.getDoubleProperty("tp2 s")
  tp3_s = graph.getDoubleProperty("tp3 s")
  tp4_s = graph.getDoubleProperty("tp4 s")
  tp5_s = graph.getDoubleProperty("tp5 s")
  tp6_s = graph.getDoubleProperty("tp6 s")
  tp7_s = graph.getDoubleProperty("tp7 s")
  tp8_s = graph.getDoubleProperty("tp8 s")
  tp9_s = graph.getDoubleProperty("tp9 s")
  viewBorderColor = graph.getColorProperty("viewBorderColor")
  viewBorderWidth = graph.getDoubleProperty("viewBorderWidth")
  viewColor = graph.getColorProperty("viewColor")
  viewFont = graph.getStringProperty("viewFont")
  viewFontSize = graph.getIntegerProperty("viewFontSize")
  viewIcon = graph.getStringProperty("viewIcon")
  viewLabel = graph.getStringProperty("viewLabel")
  viewLabelBorderColor = graph.getColorProperty("viewLabelBorderColor")
  viewLabelBorderWidth = graph.getDoubleProperty("viewLabelBorderWidth")
  viewLabelColor = graph.getColorProperty("viewLabelColor")
  viewLabelPosition = graph.getIntegerProperty("viewLabelPosition")
  viewLayout = graph.getLayoutProperty("viewLayout")
  viewMetric = graph.getDoubleProperty("viewMetric")
  viewRotation = graph.getDoubleProperty("viewRotation")
  viewSelection = graph.getBooleanProperty("viewSelection")
  viewShape = graph.getIntegerProperty("viewShape")
  viewSize = graph.getSizeProperty("viewSize")
  viewSrcAnchorShape = graph.getIntegerProperty("viewSrcAnchorShape")
  viewSrcAnchorSize = graph.getSizeProperty("viewSrcAnchorSize")
  viewTexture = graph.getStringProperty("viewTexture")
  viewTgtAnchorShape = graph.getIntegerProperty("viewTgtAnchorShape")
  viewTgtAnchorSize = graph.getSizeProperty("viewTgtAnchorSize")
  
  tp = [tp1_s,tp2_s,tp3_s,tp4_s,tp5_s,tp6_s,tp7_s,tp8_s,tp9_s,tp10_s,tp11_s,tp12_s,tp13_s,tp14_s ,tp15_s ,tp16_s ,tp17_s]

  # Note: It is recommended to execute each function one by one to have good results (by putting # before each function call that are not used)
  # Part 1
#  setGraphLayout(graph, viewLabel, Locus, viewSize, viewColor, Positive, Negative, viewLayout)
  
  # Part 2
#  displayHierarchicalTree(graph, viewMetric, viewColor) 
#  createBundles(graph, viewLayout, viewShape)
  
  # Part 3
#  displaySmallImages(graph, tp, viewColor, 5)

  
#--------------------------------------------------------  
  # Part 4
#  getClusters(graph)
#  getAllLocus(graph, Locus)
  
    
