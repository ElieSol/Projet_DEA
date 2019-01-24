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
  
#
#
#
#
#

def dfs_recursive(g, node, racine, path=[]): 
  path += [node]
  if node==racine:
  	return path    
  for neighbor in g.getInOutNodes (node): 
  	print("The neighbour of node: ",node,"is",neighbor)
  	if neighbor == racine:
  		print("Root found")
  		break
  		return path
  	if neighbor in path:
  		print("neigbor in path")
  		print(path)
  		break
  		return path
  		break
  	else:
	  	path = dfs_recursive(g, neighbor, racine, path) 
  return path 

def findShortestPath (g, node_start, node_end,racine):
	viewColor = graph.getColorProperty("viewColor")
	viewSize = graph.getSizeProperty("viewSize")
	viewShape = graph.getIntegerProperty("viewShape")
	baseSize = tlp.Size(20,20,20)
	pathFromRoot=dfs_recursive (g,node_end,racine, path=[])
	pathFromRoot.pop(len(pathFromRoot)-1)
	racine=pathFromRoot.pop(len(pathFromRoot)-1)
	print("new racine =",racine)
	print("pathFromRoot=",pathFromRoot)
	pathToRoot=dfs_recursive (g,node_start,racine, path=[])
	print("pathToRoot=", pathToRoot)
	pathFromRoot=pathFromRoot[::-1]
	print("pathFromRootReverse=",pathFromRoot)
	pathToRootf = pathToRoot+[racine]
	print("pathToRoot=", pathToRootf)
	finalPath=pathToRootf+pathFromRoot
	print("final path is =", finalPath)
	for node in finalPath:
		viewColor[node]=tlp.Color.Violet
		viewSize[node] = baseSize
		viewShape[node] = tlp.NodeShape.Square


	return finalPath
#
#
#
#
#
def createBundles(g, gLayout):
  for edge in g.getEdges():
    print (edge)
    list_node = []
    i=0
    for n in g.getNodes():
      list_node.append(n) 
      i+=1  
    shortestpath=findShortestPath(g, list_node[2], list_node[5], list_node[0])
    #shortestpath=findShortestPath(g,g.source(edge), g.target(edge),path=[])
    nodesPath=[]
    for node in shortestpath:
      nodesPath.append(gLayout[node])
    gLayout.setEdgeValue(edge,nodesPath)
  shape.setAllEdgeValue(16)


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
  
  #question 2.1
  tree = graph.addSubGraph("Hierarchical Tree")
  racine = tree.addNode()
  genes_interaction= graph.getSubGraph("Genes interactions")
  cluster= genes_interaction.getSubGraphs()
  createHierarchicalTree(tree,racine,cluster)

  # question 2.2
  getRadialTreeVersion(graph.getSubGraph("Hierarchical Tree"))
  
  colorNodes(graph.getSubGraph("Hierarchical Tree"), viewMetric, viewColor)

  list_node = []
  
  for n in graph.getNodes():
    list_node.append(n)
  

  #print(findShortestPath(tree, tree.getOneNode(), list_node[5],path=[]))
  createBundles(genes_interaction, viewLayout)
