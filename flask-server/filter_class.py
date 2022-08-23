from event_log import EventLog

class Filter:

    def filter(self, eventLog, **parameters) -> EventLog:
        pass

    def get_name(self) -> str:
        return "NAME not DEFIEND"

class FilterOut(Filter):

    def __init__(self):
        super().__init__()
        self.name = "filterOut"

    def filter(self, eventLog, **parameters):
        activityClass = parameters
        # TODO

    def get_name(self):
        return self.name