#include <iostream>
#include <vector>
#include "utils.h"      // Include utils namespace for process generation
#include "scheduler.h"  // Include Scheduler class definition
#include "process.h"

int main() {
    // Parameters for generating random processes
    int numProcesses = 5;
    int maxBurstTime = 10;
    int maxPriority = 5;

    // Generate a vector of random processes using utils namespace
    std::vector<Process> processes = Utils::generateRandomProcesses(numProcesses, maxBurstTime, maxPriority);

    // Display the generated processes
    std::cout << "Generated Processes:" << std::endl;
    for (const auto& process : processes) {
        std::cout << process << std::endl;
    }
    std::cout << std::endl;

    // Create a Scheduler instance with the generated processes
    Scheduler scheduler(processes);

    // Simulate FCFS scheduling algorithm
    std::cout << "Simulating FCFS Scheduling..." << std::endl;
    scheduler.runFCFS();

    return 0;
}
