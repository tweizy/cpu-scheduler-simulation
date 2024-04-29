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
    for process in processes:
        total_turnaround_time += (process.get_finish_time() - process.get_arrival_time())
    return total_turnaround_time / len(processes)

def calculate_average_waiting_time(processes):
    total_waiting_time = 0.0
    for process in processes:
        total_waiting_time += ((process.get_finish_time() - process.get_burst_time()) - process.get_arrival_time())
    return total_waiting_time / len(processes)
