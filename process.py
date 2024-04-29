class Process:
    def __init__(self, id, arrival_time, burst_time, priority=None):
        self.id = id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.finish_time = None
    
    def get_id(self):
        return self.id

    def get_arrival_time(self):
        return self.arrival_time

    def get_burst_time(self):
        return self.burst_time

    def get_priority(self):
        return self.priority

    def get_finish_time(self):
        return self.finish_time

    def set_finish_time(self, finish_time):
        self.finish_time = finish_time
    
    def __str__(self):
        return f"Process ID: {self.id}, Arrival Time: {self.arrival_time}, Burst Time: {self.burst_time}, Priority: {self.priority}, Finish Time: {self.finish_time}"
