class Process:
    def __init__(self, id, arrival_time, burst_time, priority=None):
        self.id = id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.finish_time = None


