from process import Process
from scheduler import Scheduler
from utils import *

def read_processes_from_file(file_path):
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


# Create a list of processes
# processes = [
#     Process(id=1, arrival_time=0, burst_time=7, priority=1),
#     Process(id=2, arrival_time=1, burst_time=4, priority=2),
#     Process(id=3, arrival_time=2, burst_time=15, priority=3),
#     Process(id=4, arrival_time=3, burst_time=11, priority=3),
#     Process(id=5, arrival_time=4, burst_time=20, priority=3),
#     Process(id=6, arrival_time=4, burst_time=9, priority=3),
# ]

processes = read_processes_from_file("processes.txt")

for process in processes:
    print(process)

# Create a scheduler instance and run the FCFS algorithm
scheduler = Scheduler(processes)
# scheduler.run_FCFS()
# scheduler.run_SJF()
# scheduler.run_priority_scheduling()
scheduler.run_round_robin(2)
# scheduler.run_priority_rr()

# Alternatively, you can call the display_results method to print out the results
# scheduler.display_results()
