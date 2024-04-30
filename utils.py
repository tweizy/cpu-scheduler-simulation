import random
from process import Process

def generate_random_processes(num_processes, max_burst_time, max_priority):
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
    total_turnaround_time = 0.0
    print("Turnaround:")
    for process in processes:
        print(f"{process.finish_time - process.arrival_time} + ")
        total_turnaround_time += (process.finish_time - process.arrival_time)

    return total_turnaround_time / len(processes)

def calculate_total_turnaround_time(processes):
    total_turnaround_time = 0.0
    print("Turnaround:")
    for process in processes:
        print(f"{process.finish_time - process.arrival_time} + ")
        process.turnaround = process.finish_time - process.arrival_time
        total_turnaround_time += (process.finish_time - process.arrival_time)
    return total_turnaround_time

def calculate_average_waiting_time(processes):
    total_waiting_time = 0.0
    print("Waiting time:")
    for process in processes:
        print(f"{(process.finish_time - process.arrival_time) - process.burst_time} + ")
        process.waiting = (process.finish_time - process.arrival_time) - process.burst_time
        total_waiting_time += (process.finish_time - process.arrival_time) - process.burst_time
    return total_waiting_time / len(processes)
def calculate_total_waiting_time(processes):
    total_waiting_time = 0.0
    print("Waiting time:")
    for process in processes:
        print(f"{(process.finish_time - process.arrival_time) - process.burst_time} + ")
        total_waiting_time += (process.finish_time - process.arrival_time) - process.burst_time
    return total_waiting_time
def find_process_by_id(process_id, processes):
    """Find a process by its ID."""
    for process in processes:
        if process.id == process_id:
            return process
    return None
