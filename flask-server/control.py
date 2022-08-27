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
        return str({"levels": self.graph.getCleanGraph(), "edges": self.graph.getEdges()}).replace("\'", "\"")

    def getEventLog(self):
        return str({"logId": self.graph.lastNode, "eventLog": self.graph.getEventLogFromId(self.graph.lastNode)}).replace("\'", "\"")

    def changeLastNode(self, json):
        print(json)
        self.graph.lastNode = json["id"]
