



 #DEPENDENCIES:  
from rawLog import rawlog

 
import datetime
import csv


class Event:
    def __init__(self, time, activity, *resources):
        self.time = time
        self.activity = activity
        self.resources = resources

    def __repr__(self):
        return f"Event {self.time}"

    def __str__(self):
        return f"Event {self.time}"

    def copy(self):
        return Event(self.time, self.activity, self.resources)

    def getForDisplay(self, headers):
        event = []
        for h in headers:
            if h == "trace":
                pass
            elif h == "activity":
                event.append(self.activity)
            elif h == "time":
                event.append(self.time)
            else:
                event.append(self.resources[h])
        return event


class Trace:
    def __init__(self, id):
        self.events = []
        self.id = id

    def addEvent(self, time, activity, *resources):
        if len(self.events) == 0 or self.events[-1].time < time:
            self.events.append(Event(time, activity, *resources))
        else:
            middle = len(self.events) // 2
            top = len(self.events) - 1
            bottom = 0
            index = self.insertIndex(middle, top, bottom, time)
            self.events.insert(index, Event(time, activity, *resources))

    def insertIndex(self, middle, top, bottom, time):
        if bottom == top:
            return top
        elif self.events[middle].time < time:
            bottom = middle + 1
            middle = (top - middle) // 2 + bottom
            return self.insertIndex(middle, top, bottom, time)
        elif self.events[middle].time > time:
            top = middle
            middle = (middle - bottom) // 2 + bottom
            return self.insertIndex(middle, top, bottom, time)
        else:
            return middle

    def removeEvents(self, indices):
        for counter, index in enumerate(indices):
            self.events.pop(index - counter)

    def __str__(self):
        return f"Trace[id:{self.id}, n_events: {len(self.events)}]"

    def getHash(self):
        # NOTE The names of the traces matter
        return f"{self.id}{len(self.events)}"

    def __repr__(self):
        return f"Trace[id:{self.id}, n_events: {len(self.events)}]"

    def copy(self):
        copyTrace = Trace(self.id)
        for event in self.events:
            copyTrace.events.append(event.copy())
        return copyTrace

    def getAsList(self, traces, id, headers):
        for event in self.events:
            e = event.getForDisplay(headers)
            e.insert(0, id)
            traces.append(e)


class EventLog:

    def __init__(self):
        self.traces = []

    def traceAlreadyPresent(self, id):
        for trace in self.traces:
            if trace.id == id:
                return True, trace
        return False, Trace(id)

    def export(self, fname):
        with open(fname, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['TraceID', 'Activity', 'Time'])
            for trace in self.traces:
                for event in trace.events:
                    writer.writerow([trace.id, event.activity, event.time])

    def convert_to_seconds(self, time, time_string, number_chars_timestamp):
        t = datetime.datetime.strptime(
            time[0:number_chars_timestamp], time_string)
        final_t = (t - datetime.datetime(1900, 1, 1)) / \
            datetime.timedelta(seconds=1)
        return final_t

    def populateTracesFromCSV(self, csvFile, timestring, timeColumn, activityColumn, traceColumn):
        for event in csvFile:
            if event[list(event.keys())[traceColumn]] != "":  # filter out empty lines
                traceIsPresent, trace = self.traceAlreadyPresent(
                    event[list(event.keys())[traceColumn]])
                if not traceIsPresent:
                    self.traces.append(trace)
                trace.addEvent(
                    self.convert_to_seconds(
                        event[list(event.keys())[timeColumn]], timestring, 18),  # time in seconds
                    event[list(event.keys())[activityColumn]])  # activity
                # extra resources need to be added

    def __repr__(self):
        string = "EventLog: \n"
        for trace in self.traces:
            string += "- " + str(trace) + "\n"
        return string

    def copy(self):
        copyEventLog = EventLog()
        for trace in self.traces:
            copyEventLog.traces.append(trace.copy())
        return copyEventLog

    def getAsList(self):
        headers = ["trace", "activity", "time"]
        traces = []
        tracesNames = []
        for trace in self.traces:
            trace.getAsList(traces, trace.id, headers)
            tracesNames.append(trace.id)
        result = {"traces": traces, "headers": headers,
                  "tracesNames": tracesNames}

        return result

    def getDescription(self):
        return self.__repr__()

path = " type in your path here "
eventlog = EventLog()
eventlog.populateTracesFromCSV(
rawlog, "%Y-%m-%dT%H:%M:%S", 3, 5, 0)
eventlog.export("final.csv")