class Process:
    """
    Represents a process in a CPU scheduling simulation.
    """

    def __init__(self, id, arrival_time, burst_time, priority=None):
        """
        Initialize a process with its attributes.

        Args:
            id (int): The unique identifier of the process.
            arrival_time (int): The time at which the process arrives.
            burst_time (int): The amount of CPU time required by the process to complete.
            priority (int, optional): The priority of the process. Defaults to None.
        """
        self.id = id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.finish_time = None

    @staticmethod
    def sort_by_id(processes):
        """
        Sorts a list of processes by their IDs.

        Args:
            processes (list): List of Process objects.

        Returns:
            list: List of Process objects sorted by ID.
        """
        return sorted(processes, key=lambda x: x.id)

    def to_dict(self):
        """
        Convert the process attributes to a dictionary.

        Returns:
            dict: Dictionary containing process attributes.
        """
        return {
            'process_id': self.id,
            'arrival_time': self.arrival_time,
            'burst_time': self.burst_time,
            'priority': self.priority
        }

    def __str__(self):
        """
        String representation of the process.

        Returns:
            str: String containing process attributes.
        """
        return f"Process ID: {self.id}, Arrival Time: {self.arrival_time}, Burst Time: {self.burst_time}, Priority: {self.priority}, Finish Time: {self.finish_time}"
