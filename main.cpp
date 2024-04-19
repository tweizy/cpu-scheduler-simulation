#include "Scheduler.h"
#include <iostream>

int main() {
    // Example: Create a vector of processes (you can replace this with input reading logic)
    std::vector<Process> processes = {
        Process(1, 0, 10, 2),
        Process(2, 2, 5, 1),
        Process(3, 3, 7, 3),
        Process(4, 5, 3, 4)
    };

    // Create a scheduler and run scheduling algorithms
    Scheduler scheduler(processes);
    scheduler.runFCFS();
    scheduler.runSJF();
    scheduler.runPriorityScheduling();
    scheduler.runRoundRobin(2);
    scheduler.runPriorityRR(2);

    return 0;
}
