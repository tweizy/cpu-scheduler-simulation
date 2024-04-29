#ifndef SCHEDULER_H
#define SCHEDULER_H

#include "process.h"
#include <vector>

class Scheduler {
public:
    Scheduler(const std::vector<Process>& processes);
    void runFCFS();
    void runSJF();
    void runPriorityScheduling();
    void runRoundRobin(int timeSlice);
    void runPriorityRR(int timeSlice);

private:
    std::vector<Process> processes;
};

#endif
