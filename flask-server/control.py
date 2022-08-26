from event_log import EventLog
from logs_graph import Graph
from filter_class import FilterOut


class Control():

    def __init__(self):
        self.currentEventLog = EventLog()  # Maybe this is not needed
        self.graph = None
        self.filters = self.initFilters()

    def loadRawfile(self, json):
        self.currentEventLog.populateTracesFromCSV(
            json["content"]["data"], json["timestampformat"], json["timestampcolumn"], json["activitycolumn"], json["tracecolumn"])
        self.graph = Graph(self.currentEventLog)
        print(self.currentEventLog)

    def initFilters(self):
        return [FilterOut()]

    # maybe the filter is going to be json format, the idea of the code should still hold
    def applyFilter(self, json):
        print(json)
        # something else  json with id: , filtertype:, parater:,
        id = json["id"]
        for filter in self.filters:
            # is not going to be just like this couse filter most probably holds also the parameters
            if filter.getName() == json["filterName"]:
                allOperations = json["previousOperations"]
                allOperations.append(filter.getName() + json["activityName"])
                print(allOperations)
                self.graph.addOperation(
                    currentNode = self.graph.getNodefromId(id),
                    operations = allOperations,
                    newEventLog = filter.filter(self.graph.getNodefromId(id).eventLog.copy(), json["activityName"], json["activityName"])
                )
                break

    def getEdgesAsJson(self):
        return str({"levels": self.graph.getCleanGraph(), "edges": self.graph.getEdges()}).replace("\'", "\"")
