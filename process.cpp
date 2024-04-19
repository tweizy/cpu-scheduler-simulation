#include "process.h"

Process::Process(int id, int arrivalTime, int burstTime, int priority)
    : id(id), arrivalTime(arrivalTime), burstTime(burstTime), priority(priority) {}

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
