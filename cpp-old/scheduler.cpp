#include<iostream>
#include "scheduler.h"
#include "utils.h"
#include <algorithm>
#include <queue>

Scheduler::Scheduler(const std::vector<Process>& processes)
    : processes(processes) {}

void Scheduler::runFCFS() {
    // Sort processes based on arrival time (assuming processes vector is already populated)
    std::sort(processes.begin(), processes.end(), [](const Process& a, const Process& b) {
        return a.getArrivalTime() < b.getArrivalTime();
    });

    int currentTime = 0;
    for (auto& process : processes) {
        // Ensure current time is at least the arrival time of the current process
        if (currentTime < process.getArrivalTime()) {
            currentTime = process.getArrivalTime();
        }

        // Execute the process
        std::cout << "Executing Process " << process.getId() << " at Time " << currentTime << std::endl;

        // Update current time to account for process burst time
        currentTime += process.getBurstTime();

        // Set finish time of the process
        process.setFinishTime(currentTime);

        // Calculate and display turnaround time for the process
        int turnaroundTime = process.getFinishTime() - process.getArrivalTime();
        std::cout << "Process " << process.getId() << " completed. Turnaround Time: " << turnaroundTime << std::endl;
    }

    // Calculate and display average turnaround time for all processes
    double avgTurnaroundTime = Utils::calculateAverageTurnaroundTime(processes);
    double avgWaitingTime = Utils::calculateAverageWaitingTime(processes);
    std::cout << "Average Turnaround Time (FCFS): " << avgTurnaroundTime << std::endl;
    std::cout << "Average Waiting Time (FCFS): " << avgWaitingTime << std::endl;
}

// void Scheduler::runSJF() {
//     // Sort processes based on burst time (shortest burst time first)
//     std::sort(processes.begin(), processes.end(), [](const Process& a, const Process& b) {
//         return a.getBurstTime() < b.getBurstTime();
//     });

//     int currentTime = 0;
//     for (auto& process : processes) {
//         // Ensure current time is at least the arrival time of the current process
//         if (currentTime < process.getArrivalTime()) {
//             currentTime = process.getArrivalTime();
//         }

//         // Execute the process
//         std::cout << "Executing Process " << process.getId() << " at Time " << currentTime << std::endl;

//         // Update current time to account for process burst time
//         currentTime += process.getBurstTime();

//         // Set finish time of the process
//         process.setFinishTime(currentTime);

//         // Calculate and display turnaround time for the process
//         int turnaroundTime = process.getFinishTime() - process.getArrivalTime();
//         std::cout << "Process " << process.getId() << " completed. Turnaround Time: " << turnaroundTime << std::endl;
//     }

//     // Calculate and display average turnaround time for all processes
//     double avgTurnaroundTime = Utils::calculateAverageTurnaroundTime(processes);
//     double avgWaitingTime = Utils::calculateAverageWaitingTime(processes);
//     std::cout << "Average Turnaround Time (SJF): " << avgTurnaroundTime << std::endl;
//     std::cout << "Average Waiting Time (SJF): " << avgWaitingTime << std::endl;
// }

void Scheduler::runSJF() {
    // Sort processes based on arrival time and burst time
    std::sort(processes.begin(), processes.end(), [](const Process& a, const Process& b) {
        if (a.getArrivalTime() == b.getArrivalTime()) {
            return a.getBurstTime() < b.getBurstTime(); // Sort by burst time if arrival times are the same
        }
        return a.getArrivalTime() < b.getArrivalTime(); // Otherwise, sort by arrival time
    });

    int currentTime = 0;
    int numProcesses = processes.size();
    int index = 0;

    while (index < numProcesses) {
        // Find processes that have arrived by the current time
        std::vector<Process> availableProcesses;
        while (index < numProcesses && processes[index].getArrivalTime() <= currentTime) {
            availableProcesses.push_back(processes[index]);
            index++;
        }

        if (availableProcesses.empty()) {
            // No processes are available yet, move time forward to the next arrival
            currentTime = processes[index].getArrivalTime();
            continue;
        }

        // Sort available processes by burst time (shortest job first)
        std::sort(availableProcesses.begin(), availableProcesses.end(), [](const Process& a, const Process& b) {
            return a.getBurstTime() < b.getBurstTime();
        });

        // Execute the shortest job (first process in the sorted list)
        Process& shortestJob = availableProcesses.front();
        std::cout << "Executing Process " << shortestJob.getId() << " at Time " << currentTime << std::endl;

        // Update current time to account for process burst time
        currentTime += shortestJob.getBurstTime();

        // Set finish time of the process
        shortestJob.setFinishTime(currentTime);

        // Calculate and display turnaround time for the process
        int turnaroundTime = shortestJob.getFinishTime() - shortestJob.getArrivalTime();
        std::cout << "Process " << shortestJob.getId() << " completed. Turnaround Time: " << turnaroundTime << std::endl;
    }

    // Calculate and display average turnaround time for all processes
    double avgTurnaroundTime = Utils::calculateAverageTurnaroundTime(processes);
    double avgWaitingTime = Utils::calculateAverageWaitingTime(processes);
    std::cout << "Average Turnaround Time (SJF): " << avgTurnaroundTime << std::endl;
    std::cout << "Average Waiting Time (SJF): " << avgWaitingTime << std::endl;
}

void Scheduler::runPriorityScheduling() {
    // Sort processes based on priority (higher priority first)
    std::sort(processes.begin(), processes.end(), [](const Process& a, const Process& b) {
        return a.getPriority() > b.getPriority(); // Sort in descending order of priority
    });

    int currentTime = 0;
    for (auto& process : processes) {
        // Ensure current time is at least the arrival time of the current process
        if (currentTime < process.getArrivalTime()) {
            currentTime = process.getArrivalTime();
        }

        // Execute the process
        std::cout << "Executing Process " << process.getId() << " at Time " << currentTime << std::endl;

        // Update current time to account for process burst time
        currentTime += process.getBurstTime();

        // Set finish time of the process
        process.setFinishTime(currentTime);

        // Calculate and display turnaround time for the process
        int turnaroundTime = process.getFinishTime() - process.getArrivalTime();
        std::cout << "Process " << process.getId() << " completed. Turnaround Time: " << turnaroundTime << std::endl;
    }

    // Calculate and display average turnaround time for all processes
    double avgTurnaroundTime = Utils::calculateAverageTurnaroundTime(processes);
    double avgWaitingTime = Utils::calculateAverageWaitingTime(processes);
    std::cout << "Average Turnaround Time (Priority Scheduling): " << avgTurnaroundTime << std::endl;
    std::cout << "Average Waiting Time (Priority Scheduling): " << avgWaitingTime << std::endl;
}

void Scheduler::runRoundRobin(int timeSlice) {
    // Implement Round Robin scheduling algorithm with the given time slice
    // ...
}

void Scheduler::runPriorityRR(int timeSlice) {
    // Implement Priority Scheduling + Round Robin algorithm with the given time slice
    // ...
}
