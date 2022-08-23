class Event:
    def __init__(self, time, activity, **resources):
        self.time = time
        self.activity = activity
        self.resources = resources

    def __repr__(self):
        return f"Event{self.time}"

    def __str__(self):
        return f"Event{self.time}"


class Trace:
    def __init__(self, id):
        self.events = []
        self.id = id

    def addEvent(self, time, activity, **resources):
        if len(self.events) == 0 or self.events[-1].time < time:
            self.events.append(Event(time, activity, **resources))
        else:
            middle = len(self.events) // 2
            top = len(self.events) - 1
            bottom = 0
            index = self.insertIndex(middle, top, bottom, time)
            self.events.insert(index, Event(time, activity, **resources))

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

    def removeEvents(indices):
        pass
        # TODO remove events in order


class EventLog:

    def __init__(self):
        self.traces = []

    def populateTracesFromCSV(self, csvFile):
        pass
        # TODO
