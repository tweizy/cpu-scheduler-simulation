#include "scheduler.h"
#include <algorithm>
#include <queue>

Scheduler::Scheduler(const std::vector<Process>& processes)
    : processes(processes) {}

void Scheduler::runFCFS() {
    // Implement First-Come, First-Served scheduling algorithm
    // ...
}

void Scheduler::runSJF() {
    // Implement Shortest Job First scheduling algorithm
    // ...
}

void Scheduler::runPriorityScheduling() {
    // Implement Priority Scheduling algorithm
    // ...
}

void Scheduler::runRoundRobin(int timeSlice) {
    // Implement Round Robin scheduling algorithm with the given time slice
    // ...
}

void Scheduler::runPriorityRR(int timeSlice) {
    // Implement Priority Scheduling + Round Robin algorithm with the given time slice
    // ...
}
