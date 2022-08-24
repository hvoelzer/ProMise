#An eventLog has to be a set of all traces

class Node: #alias Log

    def __init__(self, eventLog, id):
        self.eventLog = eventLog
        self.hash = self.hashNode()
        self.id = id

    def hashNode(self):
        hash = ""
        traces = self.eventLog.traces # NOTE maybe since the order of the traces should not matter they should be ordered with respect to the alphabetical order of the ids
        for trace in traces:
            hash += trace.getHash() # NOTE all equivalent event-log must have the same hash
        return hash

class Edge:

    def __init__(self, parentNode, operation, childrenNode):
        self.parentNode = parentNode
        self.operation = operation
        self.childrenNode = childrenNode


class Graph:

    def __init__(self, eventLog):
        self.root = Node(eventLog.copy(), 0)  #maybe it is not needed
        self.nodes = [self.root]
        self.edges = []

    #Whenever a diff (filter) is created we need to generate a new node
    def createNewEdge(self, currentNode, newEventLog, operation):  # operation or diff/filter that has been applied
        newNodeNotChecked = Node(newEventLog, len(self.nodes)) # NOTE is going to be a problem if we delete nodes
        newNode = self.checkForMatch(newNodeNotChecked) # check if node already exists
        self.edges.append(Edge(currentNode, operation, newNode))


    # returns the new node or the equivalent old one
    def checkForMatch(self, newNode):
        for node in self.nodes:
            if node.hash == newNode.hash:
                if True: # TODO here we need a further check, maybe done line by line in each trace between the two eventlogs
                    return node
        self.nodes.append(newNode)
        return newNode

    def getNodefromId(self, id):
        return self.nodes[id]

    def getEdges(self):
        result = []
        for edge in self.edges:
            result.append({"parentNode":edge.parentNode.id, "childrenNode":edge.childrenNode.id, "operation":edge.operation})
