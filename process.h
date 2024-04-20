#include<iostream>
#ifndef PROCESS_H
#define PROCESS_H

class Process {
public:
    Process(int id, int arrivalTime, int burstTime, int priority);
    int getId() const;
    int getArrivalTime() const;
    int getBurstTime() const;
    int getPriority() const;
    int getFinishTime() const;
    void setFinishTime(int finishTime);

private:
    int id;
    int arrivalTime;
    int burstTime;
    int priority;
    int finishTime;
};

// Overload the << operator to print Process information
std::ostream& operator<<(std::ostream& os, const Process& process);

#endif