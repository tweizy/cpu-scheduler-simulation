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
    std::cout << "Average Turnaround Time (FCFS): " << avgTurnaroundTime << std::endl;
}

void Scheduler::runSJF() {
    // Sort processes based on burst time (shortest burst time first)
    std::sort(processes.begin(), processes.end(), [](const Process& a, const Process& b) {
        return a.getBurstTime() < b.getBurstTime();
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
    std::cout << "Average Turnaround Time (SJF): " << avgTurnaroundTime << std::endl;
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
    std::cout << "Average Turnaround Time (Priority Scheduling): " << avgTurnaroundTime << std::endl;
}

void Scheduler::runRoundRobin(int timeSlice) {
    // Implement Round Robin scheduling algorithm with the given time slice
    // ...
}

void Scheduler::runPriorityRR(int timeSlice) {
    // Implement Priority Scheduling + Round Robin algorithm with the given time slice
    // ...
}
