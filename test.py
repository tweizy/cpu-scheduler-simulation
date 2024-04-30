from process import Process
from scheduler import Scheduler
from utils import *

# Create a list of processes manually
processes_manual = [
     Process(id=1, arrival_time=1, burst_time=1, priority=1),
     Process(id=2, arrival_time=1, burst_time=1, priority=2),
]

# Reading processes from processes2.txt file in the same directory
processes_file = read_processes_from_file("processes2.txt")

# Printing information about all of the processes
for process in processes_file:
   print(process)

# Create a scheduler instance and run the FCFS algorithm
scheduler = Scheduler(processes_file)
scheduler.run_FCFS()
# scheduler.run_SJF()
# scheduler.run_priority_scheduling()
# scheduler.run_round_robin(2)
# scheduler.run_round_robin_priority(4)