from event_log import EventLog


class Filter:

    def __init__(self, *parameters) -> None:
        self.parameters = parameters
        self.name = "NAME not DEFIEND"

    def filter(self, eventLog) -> EventLog:
        pass

    def getName(self) -> str:
        return self.name + self.parameters[0]

    def getDict(self):
        return {"filterName": self.name, "activityName": self.parameters[0]}

    def __hash__(self):
        return hash((self.name, self.parameters))

    def __eq__(self, filter) -> bool:
        return self.name == filter.name and self.parameters == filter.parameters

    def get_function(self) -> str:
        pass

    def get_comment(self) -> str:
        pass

    @staticmethod
    def generateFilter(*parameters):
        pass


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

    def get_function(self, varnumber):
        return """for trace in eventlog.traces:
            indicesToRemove = []
            for count, event in enumerate(trace.events):
                if event.activity == filterout{}:
                    indicesToRemove.append(count)
            trace.removeEvents(indicesToRemove)""".format(varnumber), ["filterout{}".format(varnumber)], ["\"" + self.parameters[0] + "\""]

    def get_comment(self):
        return "#This filters out activity {}.".format(self.parameters[0])

    @staticmethod
    def generateFilter(*parameters):
        return FilterOut(*parameters)
