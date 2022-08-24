from event_log import EventLog

class Filter:

    def filter(self, eventLog, *parameters) -> EventLog:
        pass

    def getName(self) -> str:
        return "NAME not DEFIEND"

class FilterOut(Filter):

    def __init__(self):
        super().__init__()
        self.name = "filterOut"

    def filter(self, eventLog, *parameters):
        activityClass = parameters[0] #probably index 0
        for trace in eventLog.traces:
            indicesToRemove = []
            for count, event in enumerate(trace.events):
                if event.activity == activityClass:
                    indicesToRemove.append(count)
            trace.removeEvents(indicesToRemove)

    def getName(self):
        return self.name