from process import Process
from scheduler import Scheduler
from utils import *

# Create a list of processes
processes = [
    Process(id=1, arrival_time=5, burst_time=6),
    Process(id=2, arrival_time=1, burst_time=4),
    Process(id=3, arrival_time=2, burst_time=8),
]

for process in processes:
    print(process)

# Create a scheduler instance and run the FCFS algorithm
scheduler = Scheduler(processes)
scheduler.run_FCFS()

# Alternatively, you can call the display_results method to print out the results
# scheduler.display_results()
