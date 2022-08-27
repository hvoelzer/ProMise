from event_log import EventLog


class Filter:

    def __init__(self, *parameters) -> None:
        self.parameters = parameters
        self.name = "NAME not DEFIEND"

    def filter(self, eventLog) -> EventLog:
        pass

    def getName(self) -> str:
        return self.name + str(self.parameters)

    def __hash__(self):
        return hash((self.name, self.parameters))

    def __eq__(self, filter) -> bool:
        return (self.name == filter.name & self.parameters == filter.parameters)


class FilterOut(Filter):

    def __init__(self, *parameters):
        super().__init__(*parameters)
        self.name = "filterOut"

    def filter(self, eventLog):
        activityClass = self.parameters[0]  # probably index 0
        print("I am filtering:", self.parameters[0])
        for trace in eventLog.traces:
            indicesToRemove = []
            for count, event in enumerate(trace.events):
                if event.activity == activityClass:
                    indicesToRemove.append(count)
            trace.removeEvents(indicesToRemove)
        return eventLog
