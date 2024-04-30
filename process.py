class Process:
    def __init__(self, id, arrival_time, burst_time, priority=None):
        self.id = id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.finish_time = None
        self.turnaround = 0.0
        self.waiting = 0.0

    @staticmethod
    def sort_by_id(processes):
            return sorted(processes, key=lambda x: x.id)

    def to_dict(self):
        return {
            'process_id': self.id,
            'arrival_time': self.arrival_time,
            'burst_time': self.burst_time,
            'priority': self.priority
        }

