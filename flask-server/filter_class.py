from event_log import EventLog
import random

SEED = 10

class Filter:

    def __init__(self, parameters) -> None:
        self.parameters = parameters
        self.name = "NAME not DEFIEND"

    def filter(self, eventLog) -> EventLog:
        pass

    def getName(self) -> str:
        name = self.name
        for parameter in self.parameters:
            name += " " + parameter
        return name

    def getDict(self):
        return {"filterName": self.name, "activityName": self.parameters}

    def __hash__(self):
        return hash((self.name, self.parameters))

    def __eq__(self, filter) -> bool:
        return self.name == filter.name and self.parameters == filter.parameters

    def get_function(self) -> str:
        pass

    def get_comment(self) -> str:
        pass

    def parameters_to_string(self):
        parameters = ""
        for parameter in self.parameters:
            name += " and " + parameter
        return parameters[5:len(parameters)]

    @staticmethod
    def generateFilter(parameters):
        pass


class FilterOut(Filter):

    def __init__(self, parameters):
        super().__init__(parameters)
        self.name = "filterOut"

    def filter(self, eventLog):
        indicesToRemove = []
        for count, trace in enumerate(eventLog.traces):
            keep = True
            for event in trace.events:
                for par in self.parameters:
                    if event.activity == par:
                        keep = False
                if not keep:
                    indicesToRemove.append(count)
        eventLog.removeTraces(indicesToRemove)
        return eventLog
        
    def get_function(self, varnumber):
        return """indicesToRemove = []
        for count, trace in enumerate(eventLog.traces):
            keep = True
            for event in enumerate(trace.events):
                for par in filterout{}:
                    if event.activity == par:
                        keep = False
                if not keep:
                    indicesToRemove.append(count)
        eventLog.removeTraces(indicesToRemove)""".format(varnumber), ["filterout{}".format(varnumber)], self.parameters


    
    def get_comment(self):
        return f"#This filters out traces {self.parameters_to_string()}."

    @staticmethod
    def generateFilter(parameters):
        return FilterOut(parameters)


class ThroughPut(Filter):

    def __init__(self, parameters):
        super().__init__(parameters)
        self.name = "throughPut"

    def filter(self, eventLog):
        event_a = self.parameters[0]
        throughputtime = self.parameters[1]
        event_b= self.parameters[2]
        

        indicesToRemove = []
        for count, trace in enumerate(eventLog.traces):
            keep = False
            time_a = 0
            for event in enumerate(trace.events):
                if event.activity == event_a:
                    if time_a == 0:
                        time_a = event.time
                elif event.activity == event_b:
                    if (time_a != 0 & event.time - time_a > throughputtime):
                        keep = True
                        break
                if not keep:
                    indicesToRemove.append(count)
        eventLog.removeTraces(indicesToRemove)
        return eventLog
        
    def get_function(self, varnumber):
        return """indicesToRemove = []
        for count, trace in enumerate(eventLog.traces):
            keep = False
            time_a = 0
            for event in enumerate(trace.events):
                if event.activity == event_a{}:
                    if time_a == 0:
                        time_a = event.time
                elif event.activity == event_b{}:
                    if (time_a != 0 & event.time - time_a > throughputtime{}):
                        keep = True
                        break
                if not keep:
                    indicesToRemove.append(count)
        eventLog.removeTraces(indicesToRemove)""".format(varnumber), ["event_a{}".format(varnumber),"throughputtime{}".format(varnumber),"event_b{}".format(varnumber)], self.parameters


    
    def get_comment(self):
        return f"#This filters out traces based on throughput time with the following parameters: {self.parameters_to_string()}."

    @staticmethod
    def generateFilter(parameters):
        return ThroughPut(parameters)

        

class FlowSelection(Filter):

    def __init__(self, parameters):
        super().__init__(parameters)
        self.name = "flowSelection"

    def filter(self, eventLog):
        event_a = self.parameters[0]
        event_b = self.parameters[1]

        indicesToRemove = []
        for count, trace in enumerate(eventLog.traces):
            keep = False
            previous_event = None
            for event in trace.events:
                if previous_event is not None and previous_event.activity == event_a and event == event_b:
                        keep = True
                        break
                if not keep:
                    indicesToRemove.append(count)
                previous_event = event
        eventLog.removeTraces(indicesToRemove)
        return eventLog
        
    def get_function(self, varnumber):
        return """indicesToRemove = []
        for count, trace in enumerate(eventLog.traces):
            keep = False
            previous_event = None
            for event in trace.events:
                if previous_event is not None and previous_event.activity == event_a{} and event == event_b{}:
                        keep = True
                        break
                if not keep:
                    indicesToRemove.append(count)
                previous_event = event
        eventLog.removeTraces(indicesToRemove)""".format(varnumber), ["event_a{}".format(varnumber),"event_b{}".format(varnumber)], self.parameters


    
    def get_comment(self):
        return f"#This filters out traces that do not have the directly follow pattern between {self.parameters[0], self.parameters[1]}."

    @staticmethod
    def generateFilter(parameters):
        return FlowSelection(parameters)


class RemoveBehavior(Filter):

    def __init__(self, parameters):
        super().__init__(parameters)
        self.name = "removeBehavior"

    def filter(self, eventLog):
        remove = self.parameters[0]
        random.seed(SEED)

        for trace in eventLog.traces:
            indicesToRemove = []
            sample = random.sample(trace, int(len(trace) * float(remove)))
            indicesToRemove.append(sample)
            trace.removeEvents(indicesToRemove)
        return eventLog
        
    def get_function(self, varnumber):
        return """remove = self.parameters[0]
        random.seed(SEED)

        for trace in eventLog.traces:
            indicesToRemove = []
            sample = random.sample(trace, int(len(trace) * float(remove{})))
            indicesToRemove.append(sample)
            trace.removeEvents(indicesToRemove)""".format(varnumber), ["remove{}".format(varnumber)], self.parameters


    
    def get_comment(self):
        return f"#This filters out {self.parameters[0]} of each trace."

    @staticmethod
    def generateFilter(parameters):
        return RemoveBehavior(parameters)
