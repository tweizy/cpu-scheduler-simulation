from process import Process
from utils import *

class Scheduler:
    """
    Represents a CPU scheduler.
    """

    def __init__(self, processes):
        """
        Initialize the scheduler with a list of processes.

        Args:
            processes (list): List of Process objects.
        """
        self.processes = processes
        self.total_turnaround_time = 0.0
        self.total_waiting_time = 0.0
        self.avg_turnaround_time = 0.0
        self.avg_waiting_time = 0.0

    def run_FCFS(self):
        """
        Run the First-Come, First-Served (FCFS) scheduling algorithm.
        """
        # Sort processes based on arrival time
        self.processes.sort(key=lambda x: x.arrival_time)

        current_time = 0
        gantt = []

        # Execute each process in FCFS order
        for process in self.processes:
            # Ensure current time is at least the arrival time of the current process
            if current_time < process.arrival_time:
                current_time = process.arrival_time

            # Execute the process
            print(f"Executing Process {process.id} at Time {current_time}")
            gantt.append((process.id, process.burst_time))

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
        total_turnaround_time = calculate_total_turnaround_time(self.processes)
        total_waiting_time = calculate_total_waiting_time(self.processes)
        print(f"Average Turnaround Time (FCFS): {avg_turnaround_time}")
        print(f"Average Waiting Time (FCFS): {avg_waiting_time}")
        print(f"Total Turnaround Time (FCFS): {total_turnaround_time}")
        print(f"Total Waiting Time (FCFS): {total_waiting_time}")
        return gantt

    def run_SJF(self):
        """
        Run the Shortest Job First (SJF) scheduling algorithm.
        """
        # Sort processes based on arrival time
        self.processes.sort(key=lambda x: x.arrival_time)
        original = [i for i in self.processes]
        current_time = 0
        gantt = []
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

            # Ensure current time is at least the arrival time of the shortest job
            if current_time < shortest_job.arrival_time:
                current_time = shortest_job.arrival_time

            # Execute the shortest job
            print(f"Executing Process {shortest_job.id} at Time {current_time}")
            gantt.append((shortest_job.id, shortest_job.burst_time))

            # Update current time to account for process burst time
            current_time += shortest_job.burst_time

            # Set finish time of the process
            shortest_job.finish_time = current_time

            # Calculate and display turnaround time for the process
            turnaround_time = shortest_job.finish_time - shortest_job.arrival_time
            print(f"Process {shortest_job.id} completed. Turnaround Time: {turnaround_time}")

            # Remove the completed process from the list of processes
            self.processes.remove(shortest_job)
            completed_processes.append(shortest_job)

        self.processes = [i for i in original]

        # Calculate and display average turnaround time for all processes
        avg_turnaround_time = calculate_average_turnaround_time(completed_processes)
        avg_waiting_time = calculate_average_waiting_time(completed_processes)
        total_turnaround_time = calculate_total_turnaround_time(completed_processes)
        total_waiting_time = calculate_total_waiting_time(completed_processes)
        print(f"Average Turnaround Time (SJF): {avg_turnaround_time}")
        print(f"Average Waiting Time (SJF): {avg_waiting_time}")
        print(f"Total Turnaround Time (SJF): {total_turnaround_time}")
        print(f"Total Waiting Time (SJF): {total_waiting_time}")
        return gantt

    def run_priority_scheduling(self):
        """
        Run the Priority Scheduling algorithm.
        """
        # Sort processes based on arrival time and priority
        self.processes.sort(key=lambda x: (x.arrival_time, -x.priority))
        original = [i for i in self.processes]

        current_time = 0
        gantt = []
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

            # Ensure current time is at least the arrival time of the highest priority process
            if current_time < highest_priority_process.arrival_time:
                current_time = highest_priority_process.arrival_time

            # Execute the highest priority process
            print(f"Executing Process {highest_priority_process.id} at Time {current_time}")
            gantt.append((highest_priority_process.id, highest_priority_process.burst_time))

            # Update current time to account for process burst time
            current_time += highest_priority_process.burst_time

            # Set finish time of the process
            highest_priority_process.finish_time = current_time

            # Calculate and display turnaround time for the process
            turnaround_time = highest_priority_process.finish_time - highest_priority_process.arrival_time
            print(f"Process {highest_priority_process.id} completed. Turnaround Time: {turnaround_time}")

            # Remove the completed process from the list of processes
            self.processes.remove(highest_priority_process)
            completed_processes.append(highest_priority_process)

        self.processes = [i for i in original]

        # Calculate and display average turnaround time for all processes
        avg_turnaround_time = calculate_average_turnaround_time(completed_processes)
        avg_waiting_time = calculate_average_waiting_time(completed_processes)
        total_turnaround_time = calculate_total_turnaround_time(completed_processes)
        total_waiting_time = calculate_total_waiting_time(completed_processes)
        print(f"Average Turnaround Time (Priority Scheduling): {avg_turnaround_time}")
        print(f"Average Waiting Time (Priority Scheduling): {avg_waiting_time}")
        print(f"Total Turnaround Time (Priority Scheduling): {total_turnaround_time}")
        print(f"Total Waiting Time (Priority Scheduling): {total_waiting_time}")

        return gantt

    def run_round_robin(self, time_slice):
        """
        Run the Round Robin (RR) scheduling algorithm.

        Args:
            time_slice (int): The time quantum for the RR algorithm.
        """
        # Sort processes based on arrival time
        self.processes.sort(key=lambda x: x.arrival_time)
        current_time = 0
        remaining_time = [process.burst_time for process in self.processes]
        completed_processes = []
        gantt = []

        while any(remaining_time):
            executed = False  # Flag to track if any process was executed in this iteration
            for i, process in enumerate(self.processes):
                if remaining_time[i] == 0:
                    continue

                if process.arrival_time <= current_time:
                    # Execute the process for the time slice or remaining burst time, whichever is smaller
                    run_time = min(time_slice, remaining_time[i])
                    remaining_time[i] -= run_time

                    # Update current time
                    current_time += run_time

                    # Add to Gantt chart
                    gantt.append((process.id, run_time))

                    # Set finish time of the process if it completes
                    if remaining_time[i] == 0:
                        process.finish_time = current_time
                        completed_processes.append(process)

                    # Calculate and display turnaround time for the process
                    turnaround_time = process.finish_time - process.arrival_time if process.finish_time else None
                    print(
                        f"Executing Process {process.id} at Time {current_time - run_time}, Remaining Burst Time: {remaining_time[i]}, Turnaround Time: {turnaround_time}")

                    executed = True  # Process was executed in this iteration

            if not executed:
                # If no process was executed, increment current time
                current_time += 1

        # Calculate and display average turnaround time for all processes
        avg_turnaround_time = calculate_average_turnaround_time(completed_processes)
        avg_waiting_time = calculate_average_waiting_time(completed_processes)
        total_turnaround_time = calculate_total_turnaround_time(completed_processes)
        total_waiting_time = calculate_total_waiting_time(completed_processes)
        print(f"Average Turnaround Time (Round Robin): {avg_turnaround_time}")
        print(f"Average Waiting Time (Round Robin): {avg_waiting_time}")
        print(f"Total Turnaround Time (Round Robin): {total_turnaround_time}")
        print(f"Total Waiting Time (Round Robin): {total_waiting_time}")

        return gantt
