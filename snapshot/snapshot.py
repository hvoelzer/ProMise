#VARIABLES: 
SEED = 10


#Filter 0:
remove0 = 0.5

#Filter 1:
filterout1 = ['Q', 'H']

#Filter 2:
event_a2 = "D"
event_b2 = "H"

#Filter 3:
event_a3 = "D"
throughputtime3 = 600
event_b3 = "H"
mode3 = "longer"
# For using different eventlog (leave path_to_file empty to use original eventlog): 
path_to_file = "" 
timestring = ""
timeColumn = 0
activityColumn = 0
traceColumn = 0
seperator = "," 






 #DEPENDENCIES:  
from rawLog import rawlog
import random
 
import datetime
import csv


def convert_back_to_string(time, time_string):
    return datetime.datetime.fromtimestamp(time).strftime(time_string)


class Event:
    def __init__(self, time, activity, timestring, *resources):
        self.time = time
        self.activity = activity
        self.resources = resources
        self.timestring = timestring

    def __repr__(self):
        return f"Event {self.time}"

    def __str__(self):
        return f"Event {self.time}"

    def copy(self):
        return Event(self.time, self.activity, self.timestring, self.resources)

    def getForDisplay(self, headers):
        event = []
        for h in headers:
            if h == "trace":
                pass
            elif h == "activity":
                event.append(self.activity)
            elif h == "time":
                event.append(convert_back_to_string(
                    self.time, self.timestring))
            else:
                event.append(self.resources[h])
        return event


class Trace:
    def __init__(self, id, timestring):
        self.events = []
        self.id = id
        self.timestring = timestring

    def addEvent(self, time, activity, *resources):
        if len(self.events) == 0 or self.events[-1].time < time:
            self.events.append(
                Event(time, activity, self.timestring, *resources))
        else:
            middle = len(self.events) // 2
            top = len(self.events) - 1
            bottom = 0
            index = self.insertIndex(middle, top, bottom, time)
            self.events.insert(index, Event(
                time, activity, self.timestring, *resources))

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
        copyTrace = Trace(self.id, self.timestring)
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
        self.timestring = ""

    def removeTraces(self, indices):
        for counter, index in enumerate(indices):
            self.traces.pop(index - counter)

    def remove_empty_traces(self):
        traces_to_remove = []
        for i, trace in enumerate(self.traces):
            if len(trace.events) == 0:
                traces_to_remove.append(i)
        self.removeTraces(traces_to_remove)

    def traceAlreadyPresent(self, id):
        for trace in self.traces:
            if trace.id == id:
                return True, trace
        return False, Trace(id, self.timestring)

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
        return (t-datetime.datetime(1970, 1, 1, 0, 0, 0)).total_seconds()

    def populateTracesFromCSV(self, csvFile, timestring, timeColumn, activityColumn, traceColumn):
        self.traces = []
        self.timestring = timestring
        for event in csvFile:
            if event[list(event.keys())[traceColumn]] != "":  # filter out empty lines
                traceIsPresent, trace = self.traceAlreadyPresent(
                    event[list(event.keys())[traceColumn]])
                if not traceIsPresent:
                    self.traces.append(trace)
                trace.addEvent(
                    self.convert_to_seconds(
                        event[list(event.keys())[timeColumn]], timestring, 19),  # time in seconds
                    event[list(event.keys())[activityColumn]])
        # activity
        # extra resources need to be added

    def actuallyPopulateTracesFromCSV(self, csvFile, timestring, timeColumn, activityColumn, traceColumn, seperator):
        with open(csvFile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=seperator)
            self.timestring = timestring
            for line_count, event in enumerate(csv_reader):
                if line_count == 0:
                    pass
                else:
                    if event[traceColumn] != "":  # filter out empty lines
                        traceIsPresent, trace = self.traceAlreadyPresent(
                            event[traceColumn])
                        if not traceIsPresent:
                            self.traces.append(trace)
                        trace.addEvent(
                            self.convert_to_seconds(
                                event[timeColumn], timestring, 19),  # time in seconds
                            event[activityColumn])  # activity
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

    def get_total_number_events(self):
        total = 0
        for trace in self.traces:
            total += len(trace.events)
        return total

    def getDescription(self):
        return f"cases: {len(self.traces)}, events:{self.get_total_number_events()}"



eventLog = EventLog()
if (path_to_file == ""):
    eventLog.populateTracesFromCSV(
rawlog, "%Y-%m-%dT%H:%M:%S", 1, 2, 0)
else:
    eventLog.actuallyPopulateTracesFromCSV(path_to_file, timestring, timeColumn, activityColumn, traceColumn, seperator)
#This filters out 0.5 of each trace.
random.seed(SEED)
total = eventLog.get_total_number_events()
sample = random.sample(range(total), int(total * float(remove0)))
sample.sort()
seen_events = 0
for ti, trace in enumerate(eventLog.traces):
    sample_trace = [i for i in sample if i>=seen_events and i<seen_events + len(trace.events)]
    sample_trace = [number - seen_events for number in sample_trace]
    seen_events += len(trace.events)
    trace.removeEvents(sample_trace)
eventLog.remove_empty_traces()
#This filters out traces  and Q and H.
indicesToRemove = []
for count, trace in enumerate(eventLog.traces):
    bool_list = [True for _ in range(len(filterout1))]
    for event in trace.events:
        for i, par in enumerate(filterout1):
            if event.activity == par:
                bool_list[i] = False
        if sum(bool_list) == 0:
            indicesToRemove.append(count)
eventLog.removeTraces(indicesToRemove)
#This filters out traces that do not have the directly follow pattern between ('D', 'H').
indicesToRemove = []
for count, trace in enumerate(eventLog.traces):
    keep = False
    previous_event = None
    for event in trace.events:
        if previous_event is not None and previous_event.activity == event_a2 and event.activity == event_b2:
                keep = True
                break
        
        previous_event = event
    if not keep:
        indicesToRemove.append(count)
eventLog.removeTraces(indicesToRemove)
#This filters out traces based on throughput time with the following parameters:  and D and H and 600 and longer.
indicesToRemove = []
for count, trace in enumerate(eventLog.traces):
    keep = False
    time_a = 0
    for event in trace.events:
        if event.activity == event_a3:
            if mode3 == "longer":
                if time_a == 0:
                    time_a = event.time
            else:
                time_a = event.time
        elif event.activity == event_b3:
            if mode3 == "longer":
                if (time_a != 0 and event.time - time_a > int(throughputtime3)):
                    keep = True
                    break
            else:
                if (time_a != 0 and event.time - time_a < int(throughputtime3)):
                    keep = True
                    break
    if not keep:
        indicesToRemove.append(count)
eventLog.removeTraces(indicesToRemove)
eventLog.export("final.csv")