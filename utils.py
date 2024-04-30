"""
Utility functions for generating, calculating, and reading processes.
"""

import random
from process import Process

def generate_random_processes(num_processes, max_burst_time, max_priority):
    """
    Generate a list of random processes with specified attributes.

    Args:
        num_processes (int): The number of processes to generate.
        max_burst_time (int): The maximum burst time for generated processes.
        max_priority (int): The maximum priority for generated processes.

    Returns:
        list: List of randomly generated Process objects.
    """
    processes = []
    random.seed()

    for i in range(num_processes):
        process_id = i + 1
        arrival_time = random.randint(0, 9)
        burst_time = random.randint(1, max_burst_time)
        priority = random.randint(1, max_priority)
        processes.append(Process(process_id, arrival_time, burst_time, priority))

    return processes

def calculate_average_turnaround_time(processes):
    """
    Calculate the average turnaround time for a list of processes.

    Args:
        processes (list): List of Process objects.

    Returns:
        float: Average turnaround time.
    """
    total_turnaround_time = 0.0
    print("Turnaround:")
    for process in processes:
        print(f"{process.finish_time - process.arrival_time} + ")
        total_turnaround_time += (process.finish_time - process.arrival_time)

    return total_turnaround_time / len(processes)

def calculate_total_turnaround_time(processes):
    """
    Calculate the total turnaround time for a list of processes.

    Args:
        processes (list): List of Process objects.

    Returns:
        float: Total turnaround time.
    """
    total_turnaround_time = 0.0
    print("Turnaround:")
    for process in processes:
        print(f"{process.finish_time - process.arrival_time} + ")
        total_turnaround_time += (process.finish_time - process.arrival_time)
    return total_turnaround_time

def calculate_average_waiting_time(processes):
    """
    Calculate the average waiting time for a list of processes.

    Args:
        processes (list): List of Process objects.

    Returns:
        float: Average waiting time.
    """
    total_waiting_time = 0.0
    print("Waiting time:")
    for process in processes:
        print(f"{(process.finish_time - process.arrival_time) - process.burst_time} + ")
        total_waiting_time += (process.finish_time - process.arrival_time) - process.burst_time
    return total_waiting_time / len(processes)

def calculate_total_waiting_time(processes):
    """
    Calculate the total waiting time for a list of processes.

    Args:
        processes (list): List of Process objects.

    Returns:
        float: Total waiting time.
    """
    total_waiting_time = 0.0
    print("Waiting time:")
    for process in processes:
        print(f"{(process.finish_time - process.arrival_time) - process.burst_time} + ")
        total_waiting_time += (process.finish_time - process.arrival_time) - process.burst_time
    return total_waiting_time

def read_processes_from_file(file_path):
    """
    Read process information from a file and create Process objects.

    Args:
        file_path (str): The path to the file containing process information.

    Returns:
        list: List of Process objects read from the file.
    """
    processes = []
    with open(file_path, "r") as file:
        for line in file:
            attributes = line.strip().split()
            priority = None
            if int(attributes[3]) != -1:
                priority = int(attributes[3])
            process = Process(int(attributes[0]), int(attributes[1]), int(attributes[2]), priority)
            processes.append(process)
    return processes
