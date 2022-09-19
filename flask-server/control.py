from event_log import EventLog
from logs_graph import Graph
from filter_class import FilterOut, Filter


class Control():

    def __init__(self):
        self.currentEventLog = EventLog()  # Maybe this is not needed
        self.graph = None
        #self.filters = self.initFilters()
        self.filtersdict = {"filterOut": FilterOut}

    def loadRawfile(self, json):
        self.currentEventLog.populateTracesFromCSV(
            json["content"]["data"], json["timestampformat"], json["timestampcolumn"], json["activitycolumn"], json["tracecolumn"])
        self.graph = Graph(self.currentEventLog)
        print(self.currentEventLog)

    def filterFromJson(self, json):  # TODO: this method could probably be written more agile
        return self.filtersdict[json["filterName"]].generateFilter(json["activityName"])

    # maybe the filter is going to be json format, the idea of the code should still hold
    def applyFilter(self, json):
        print(json)
        # something else  json with id: , filtertype:, parater:,
        # get id of node to be filtered
        id = json["id"]
        # create filter to be applied
        filter = self.filterFromJson(json)

        allOperations = list(
            map(self.filterFromJson, json["previousOperations"]))

        allOperations.append(filter)

        self.graph.addOperation(
            currentNode=self.graph.getNodefromId(id),
            operations=allOperations,
            newEventLog=filter.filter(self.graph.getNodefromId(
                id).eventLog.copy())
        )

    def getEdgesAsJson(self):
        print(str({"levels": self.graph.getCleanGraph(),
              "edges": self.graph.getEdges()}).replace("\'", "\""))
        return str({"levels": self.graph.getCleanGraph(), "edges": self.graph.getEdges()}).replace("\'", "\"")

    def reverseGraphTrieMap(self):
        reverse = {}
        for key in self.graph.map_trie_graph.keys():
            for elemnt in self.graph.map_trie_graph[key]:
                st_elem = str(elemnt)
                reverse[st_elem] = key
        return reverse

    def getEdgesAsJsonHistory(self):
        nod, ed, hist = self.graph.getCleanGraphTrie(False)
        levels = []
        for key in nod.keys():
            levels.append({"id": int(key), "nodes": nod[key]})
        print(str({"levels": levels,
              "edges": ed}).replace("\'", "\""))
        print(self.graph.map_trie_graph)
        print("historys:", hist)
        map = self.reverseGraphTrieMap()
        print(map)
        return str({"levels": levels, "edges": ed, "map": map}).replace("\'", "\"")

    def getEventLog(self):
        log = self.graph.cleanNodeFromTrieNode(self.graph.lastNode)
        nod, ed, history = self.graph.getCleanGraphTrie(False)

        return str({"logId": self.graph.lastNode, "eventLog": self.graph.getEventLogFromId(log), "history": history[self.graph.lastNode]}).replace("\'", "\"")

    def changeLastNode(self, json):
        print(json)
        self.graph.lastNode = json["id"]

    def create_snapshot(self, json):
        fname = 'snapshot.py'
        nod, ed, history = self.graph.getCleanGraphTrie(True)

        dependencies = 'event_log.py'

        with open(dependencies, 'r') as d:
            dep_str = d.read()
            d.close()

        script = "\n\n\n\n #DEPENDENCIES:  \n\n " + dep_str
        script = script + \
            """\npath = \" type in your path here \"\neventlog = EventLog()\neventlog.populateTracesFromCSV(\njson["content"]["data"], \"timestampformat\", \"timestampcolumn\", \"activitycolumn\", \"tracecolumn\")"""

        for filter in history[json["id"]]:
            cmt = filter.get_comment()
            fct = filter.get_function()
            script = script + "\n" + cmt + "\n" + \
                fct
        print(script)

        with open(fname, 'w') as f:
            f.write(script)
            f.close()
