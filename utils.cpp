#include "utils.h"
#include "process.h"
#include <fstream>
#include <cstdlib>
#include <ctime>

namespace Utils {
    std::vector<Process> generateRandomProcesses(int numProcesses, int maxBurstTime, int maxPriority) {
        std::vector<Process> processes;
        std::srand(static_cast<unsigned int>(std::time(nullptr)));

        for (int i = 0; i < numProcesses; ++i) {
            int id = i + 1;
            int arrivalTime = std::rand() % 10; // Random arrival time between 0 and 9
            int burstTime = 1 + std::rand() % maxBurstTime; // Random burst time between 1 and maxBurstTime
            int priority = 1 + std::rand() % maxPriority; // Random priority between 1 and maxPriority
            processes.emplace_back(id, arrivalTime, burstTime, priority);
        }

        return processes;
    }


    double calculateAverageTurnaroundTime(const std::vector<Process>& processes) {
        double totalTurnaroundTime = 0.0;
        for (const auto& process : processes) {
            totalTurnaroundTime += (process.getFinishTime() - process.getArrivalTime());
        }
        return (totalTurnaroundTime / processes.size());
    }

    double calculateAverageWaitingTime(const std::vector<Process>& processes) {
        double totalWaitingTime = 0.0;
        for (const auto& process : processes) {
            totalWaitingTime += ((process.getFinishTime() - process.getBurstTime()) - process.getArrivalTime());
        }
        return (totalWaitingTime / processes.size());
    }
}
