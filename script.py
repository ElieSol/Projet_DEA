# Powered by Python 2.7

# To cancel the modifications performed by the script
# on the current graph, click on the undo button.

# Some useful keyboards shortcuts : 
#   * Ctrl + D : comment selected lines.
#   * Ctrl + Shift + D  : uncomment selected lines.
#   * Ctrl + I : indent selected lines.
#   * Ctrl + Shift + I  : unindent selected lines.
#   * Ctrl + Return  : run script.
#   * Ctrl + F  : find selected text.
#   * Ctrl + R  : replace selected text.
#   * Ctrl + Space  : show auto-completion dialog.

from tulip import tlp
from collections import deque

# The updateVisualization(centerViews = True) function can be called
# during script execution to update the opened views

# The pauseScript() function can be called to pause the script execution.
# To resume the script execution, you will have to click on the "Run script " button.

# The runGraphScript(scriptFile, graph) function can be called to launch
# another edited script on a tlp.Graph object.
# The scriptFile parameter defines the script name to call (in the form [a-zA-Z0-9_]+.py)

# The main(graph) function must be defined 
# to run the script on the current graph


# Variables

NODE_WIDTH = 12
NODE_HEIGHT = 4


##########
# Part 1 #
##########

# Function to display the labels on the network's peaks/nodes
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
      viewColor[edge] = tlp.Color.Violet
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


##########
# Part 2 #
##########

# Function to create a Hierarchical Tree
# 
# Parameters: tree (empty subgraph), root (node), cluster (list of subgraphs)
# Return: None
#

def createHierarchicalTree(tree,root,cluster):
  #if(cluster.numberOfSubGraphs()!=0):
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
# Parameters: graph, property
# Return: None
#

def colorNodes(g, property, color):
  params = tlp.getDefaultPluginParameters('Alpha Mapping', g)
  params['input property']=property
  params['target']='nodes'
  params['color scale']='BiologicalHeatMap.png'
  g.applyColorAlgorithm('Alpha Mapping', params)
  
# Function to find the shortest path between two nodes in a graph
#
# Parameters: graph, start (node1), end (node2), path (list of node in the path, empty when the function is called)
# Return: List of node in the shortest path
#

def findPath(graph, n, root, path=[]):
  path+=[n]
  if(n==root):
#    print("n==root")
    return path
  if graph.isElement(n)!=True:
    return None
  for neigbor in graph.getInOutNodes(n):
#    print("neighbour of ",n, " is :", neigbor)
    findPath(graph, neigbor, root, path)
    if(neigbor == root):
#      print("ROOT ",root," EQUALS NEIGHBOUR")
      return path;
    if(neigbor in path):
      return path
    if(neigbor!= root and neigbor not in path):
#      print("neighbour not in path")
      findPath(graph, neigbor, root, path)
  return path  

def removeDuplicate(list_1,list_2):
  match = list(set(list_1) & set(list_2))
  if len(match)<=2:
     root = match[len(match)-1]
  elif len(match)>2:
     root=match[0]
#  print("match = ",match)
  list_2=list_2[::-1]
#  print("pathway 2 after reversal =",list_2)
  for el in match:
    list_1.remove(el)
    list_2.remove(el)
  finalList = list_1 +[root]+ list_2
  return finalList

def findShortestPath(graph, n1, n2):
  viewColor = graph.getColorProperty("viewColor")
  viewSize = graph.getSizeProperty("viewSize")
  viewShape = graph.getIntegerProperty("viewShape")
  baseSize = tlp.Size(50,50,50)
  list_node = []
  tree = graph.getSubGraph("Hierarchical Tree")
  i=0
  for n in tree.getNodes():
    list_node.append(n) 
    i+=1
  root = list_node[0]
#  print(n1)
#  print(n2)
  pathway_1=findPath(tree, n1, root, path=[])
#  print("pathway 1 =",pathway_1)
  pathway_2=findPath(tree, n2, root, path=[])
#  print("pathway 2 =",pathway_2)
  pathway = removeDuplicate(pathway_1,pathway_2)
  for node in pathway:
    viewColor[node]=tlp.Color.Violet
    viewSize[node] = baseSize
    viewShape[node] = tlp.NodeShape.Square
#  print(pathway)
#  print("final pathway= ",pathway)
  return pathway

#
#
#
#
#
def createBundles(g, gLayout):
  for edge in g.getEdges():
    print("EDGE = ",edge)
    shortestpath=findShortestPath(g,g.source(edge), g.target(edge))
    nodesPath=[]
    for node in shortestpath:
      nodesPath.append(gLayout[node])
    print("path=",nodesPath)
    gLayout.setEdgeValue(edge,nodesPath)


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
   
  displayLabels(graph,viewLabel,Locus)
  setNodesSize(graph,viewSize)
  setDisplayOfEdges(graph, viewColor, Positive, Negative)
  setNodesPosition(graph, viewLayout)
  updateVisualization()

  if(graph.getSubGraph("Hierarchical Tree")!=None):
  	graph.delSubGraph(graph.getSubGraph("Hierarchical Tree"))  
  
  #question 2.1
  tree = graph.addSubGraph("Hierarchical Tree")
  racine = tree.addNode()
  genes_interaction= graph.getSubGraph("Genes interactions")
  cluster= genes_interaction.getSubGraphs()
  createHierarchicalTree(tree,racine,cluster)

  # question 2.2
  getRadialTreeVersion(graph.getSubGraph("Hierarchical Tree"))
  
  colorNodes(graph.getSubGraph("Hierarchical Tree"), viewMetric, viewColor)
  
  createBundles(graph, viewLayout)
#  viewLayout.setAllEdgeValue()
#  findShortestPath()
