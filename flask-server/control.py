from asyncio.windows_events import NULL
from warnings import filters
from event_log import EventLog
from logs_graph import Graph
from filter_class import FilterOut


class Control():

    def __init__(self):
        self.currentEventLog = EventLog()
        self.graph = NULL
        self.filters = self.initFilters()

    def load_rawfile(self, json):
        self.currentEventLog.populateTracesFromCSV(json["content"]["data"], json["timestampformat"], json["timestampcolumn"], json["activitycolumn"], json["tracecolumn"])
        self.graph = Graph(self.currentEventLog)
        print(self.currentEventLog)

    def initFilters(self):
        return [FilterOut()]

    def applyFilter(self, filter): #maybe the filter is going to be json format, the idea of the code should still hold
        for filter in self.filters:
            if filter.get_name() == filter: #is not going to be just like this couse filter most probably holds also the parameters
                self.graph.createNewNode(filter.filter(self.graph.currentNode.eventLog.copy()))
