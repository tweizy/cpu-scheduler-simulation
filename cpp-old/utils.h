#ifndef UTILS_H
#define UTILS_H

#include <vector>
#include "process.h"

namespace Utils {
    // Function to generate random processes
    std::vector<Process> generateRandomProcesses(int numProcesses, int maxBurstTime, int maxPriority);

    // Function to calculate average turnaround time
    double calculateAverageTurnaroundTime(const std::vector<Process>& processes);

    // Function to calculate average waiting time
    double calculateAverageWaitingTime(const std::vector<Process>& processes);
}

#endif
