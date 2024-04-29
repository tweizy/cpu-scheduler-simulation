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
        # Sort processes based on arrival time
        self.processes.sort(key=lambda x: x.arrival_time)
        
        current_time = 0
        completed_processes = []

        while self.processes:
            # Find processes that have arrived before or at the current time
            available_processes = [process for process in self.processes if process.arrival_time <= current_time]
            
            if not available_processes:
                # If no processes are available, move time to the next arrival time
                current_time = self.processes[0].arrival_time
                continue

            # Select the process with the minimum burst time among available processes
            shortest_job = min(available_processes, key=lambda x: x.burst_time)

            # Update current time
            current_time += shortest_job.burst_time

            # Set finish time of the process
            shortest_job.finish_time = current_time

            # Calculate and display turnaround time for the process
            turnaround_time = shortest_job.finish_time - shortest_job.arrival_time
            print(f"Executing Process {shortest_job.id} at Time {current_time - shortest_job.burst_time}")
            print(f"Process {shortest_job.id} completed. Turnaround Time: {turnaround_time}")

            # Remove the completed process from the list of processes
            self.processes.remove(shortest_job)
            completed_processes.append(shortest_job)

        # Calculate and display average turnaround time for all processes
        avg_turnaround_time = calculate_average_turnaround_time(completed_processes)
        avg_waiting_time = calculate_average_waiting_time(completed_processes)
        print(f"Average Turnaround Time (SJF): {avg_turnaround_time}")
        print(f"Average Waiting Time (SJF): {avg_waiting_time}")

    def run_priority_scheduling(self):
        # Sort processes based on arrival time and priority
        self.processes.sort(key=lambda x: (x.arrival_time, -x.priority))

        current_time = 0
        completed_processes = []

        while self.processes:
            # Find processes that have arrived before or at the current time
            available_processes = [process for process in self.processes if process.arrival_time <= current_time]
            
            if not available_processes:
                # If no processes are available, move time to the next arrival time
                current_time = self.processes[0].arrival_time
                continue

            # Select the process with the highest priority among available processes
            highest_priority_process = max(available_processes, key=lambda x: x.priority)

            # Update current time
            current_time += highest_priority_process.burst_time

            # Set finish time of the process
            highest_priority_process.finish_time = current_time

            # Calculate and display turnaround time for the process
            turnaround_time = highest_priority_process.finish_time - highest_priority_process.arrival_time
            print(f"Executing Process {highest_priority_process.id} at Time {current_time - highest_priority_process.burst_time}")
            print(f"Process {highest_priority_process.id} completed. Turnaround Time: {turnaround_time}")

            # Remove the completed process from the list of processes
            self.processes.remove(highest_priority_process)
            completed_processes.append(highest_priority_process)

        # Calculate and display average turnaround time for all processes
        avg_turnaround_time = calculate_average_turnaround_time(completed_processes)
        avg_waiting_time = calculate_average_waiting_time(completed_processes)
        print(f"Average Turnaround Time (Priority Scheduling): {avg_turnaround_time}")
        print(f"Average Waiting Time (Priority Scheduling): {avg_waiting_time}")

    def run_round_robin(self, time_slice):
        # Sort processes based on arrival time
        self.processes.sort(key=lambda x: x.arrival_time)

        current_time = 0
        remaining_time = [process.burst_time for process in self.processes]
        completed_processes = []

        while any(remaining_time):
            for i, process in enumerate(self.processes):
                if remaining_time[i] == 0 or process.arrival_time > current_time:
                    continue
                
                # Execute the process for the time slice or remaining burst time, whichever is smaller
                run_time = min(time_slice, remaining_time[i])
                remaining_time[i] -= run_time

                # Update current time
                current_time += run_time

                # Set finish time of the process if it completes
                if remaining_time[i] == 0:
                    process.finish_time = current_time
                    completed_processes.append(process)
                
                # Calculate and display turnaround time for the process
                turnaround_time = process.finish_time - process.arrival_time if process.finish_time else None
                print(f"Executing Process {process.id} at Time {current_time - run_time}, Remaining Burst Time: {remaining_time[i]}, Turnaround Time: {turnaround_time}")

        # Calculate and display average turnaround time for all processes
        avg_turnaround_time = calculate_average_turnaround_time(completed_processes)
        avg_waiting_time = calculate_average_waiting_time(completed_processes)
        print(f"Average Turnaround Time (Round Robin): {avg_turnaround_time}")
        print(f"Average Waiting Time (Round Robin): {avg_waiting_time}")
    
    def run_priority_rr(self, time_slice):
        # Implement Priority Scheduling + RR algorithm with given time slice
        pass
