#include<iostream>
#include "process.h"

Process::Process(int id, int arrivalTime, int burstTime, int priority)
    : id(id), arrivalTime(arrivalTime), burstTime(burstTime), priority(priority), finishTime(0) {}

int Process::getId() const {
    return id;
}

int Process::getArrivalTime() const {
    return arrivalTime;
}

int Process::getBurstTime() const {
    return burstTime;
}

int Process::getPriority() const {
    return priority;
}

int Process::getFinishTime() const {
    return finishTime;
}

void Process::setFinishTime(int finishTime) {
    this->finishTime = finishTime;
}

// Overload the << operator to print Process information
std::ostream& operator<<(std::ostream& os, const Process& process) {
    os << "Process ID: " << process.getId()
       << ", Arrival Time: " << process.getArrivalTime()
       << ", Burst Time: " << process.getBurstTime()
       << ", Priority: " << process.getPriority();
    return os;
}