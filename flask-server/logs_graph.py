#An eventLog has to be a set of all traces

class Node: #alias Log

    def __init__(self, eventLog):
        self.eventLog = eventLog
        self.children = []
        self.parents = []
        self.hash = self.hashNode(eventLog)

    def hashNode(eventLog):
        hash = 2 #all equivalent event-log must have the same hash
        return hash

    def addChildren(self, node):
        self.children.append(node)

    def addParent(self, node):
        self.parents.append(node)


class Graph:

    def __init__(self, eventLog):
        self.root = Node(eventLog)  #maybe it is not needed
        self.currentNode = self.root
        self.nodes = [self.root]

    #Whenever a diff (filter) is created we need to generate a new node
    def createNewNode(self, newEventLog, operation):  # operation or diff/filter that has been applied
        newNodeNotChecked = Node(newEventLog)
        newNode = self.checkForMatch(newNodeNotChecked) # check if node already exists

        self.currentNode.addChildren((newNode, operation))
        newNode.addParent((self.currentNode, operation))

        self.currentNode = newNode


    # returns the new node or the equivalent old one
    def checkForMatch(self, newNode):
        for node in self.nodes:
            if node.hash == newNode.hash:
                if True: # TODO here we need a further check, maybe done line by line in each trace between the two eventlogs
                    return node
        return newNode
                    

