#ifndef PROCESS_H
#define PROCESS_H

class Process {
public:
    Process(int id, int arrivalTime, int burstTime, int priority);
    int getId() const;
    int getArrivalTime() const;
    int getBurstTime() const;
    int getPriority() const;

private:
    int id;
    int arrivalTime;
    int burstTime;
    int priority;
};

#endif