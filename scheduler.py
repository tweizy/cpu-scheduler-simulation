from process import Process
from utils import *

class Scheduler:
    def __init__(self, processes : list[Process]):
        self.processes = processes

    def run_FCFS(self):
        # Sort processes based on arrival time
        self.processes.sort(key=lambda x: x.arrival_time)

        current_time = 0
        for process in self.processes:
            # Ensure current time is at least the arrival time of the current process
            if current_time < process.arrival_time:
                current_time = process.arrival_time

            # Execute the process
            print(f"Executing Process {process.id} at Time {current_time}")

            # Update current time to account for process burst time
            current_time += process.burst_time

            # Set finish time of the process
            process.finish_time = current_time

            # Calculate and display turnaround time for the process
            turnaround_time = process.finish_time - process.arrival_time
            print(f"Process {process.id} completed. Turnaround Time: {turnaround_time}")
        
        # Calculate and display average turnaround time for all processes
        avg_turnaround_time = calculate_average_turnaround_time(self.processes)
        avg_waiting_time = calculate_average_waiting_time(self.processes)
        print(f"Average Turnaround Time (FCFS): {avg_turnaround_time}")
        print(f"Average Waiting Time (FCFS): {avg_waiting_time}")

    def run_SJF(self):
        # Implement Shortest Job First (SJF) scheduling algorithm
        pass

    def run_priority_scheduling(self):
        # Implement Priority Scheduling algorithm
        pass

    def run_round_robin(self, time_slice):
        # Implement Round Robin (RR) scheduling algorithm with given time slice
        pass

    def run_priority_rr(self, time_slice):
        # Implement Priority Scheduling + RR algorithm with given time slice
        pass
