# cpu-scheduler-simulation
CPU scheduler simulation program that simulates the behavior of different scheduling algorithms.
## Overview
This program simulates various CPU scheduling algorithms, offering a deep dive into their functionality and impact on system performance. It supports multiple scheduling algorithms including First-Come, First-Served (FCFS), Shortest Job First (SJF), Priority Scheduling, and Round Robin (RR). This tool is designed to help users understand and compare the effectiveness of these algorithms through comprehensive visualizations and performance metrics.

## Features

Multiple Scheduling Algorithms: Simulate four different algorithms to understand their operation and efficiency.
Custom Input Options: Enter process data manually or generate random processes by specifying range limits.
Comprehensive Visualizations: Includes Gantt charts for process scheduling, bar plots for turnaround and waiting times, and comparative plots for overall performance analysis.
Flexible User Interaction: Users can select one or multiple algorithms for side-by-side performance comparison.
Dynamic Testing and Validation: Supports input from files and ensures correctness with dynamic input validations.

## Installation
Navigate to the project directory:

cd [project_directory]

## Usage
### Web App
To run the application, execute the following command in the terminal:

python app.py

### Terminal
Open the test.py file and read the documented code to understand how to use it. In this file is explained how to run algorithms on processes either by reading them from a .txt file, or manually creating processes objects. Examples are already provided to provided further explanation.

## Main menu
Upon launching, the main menu allows you to choose how to input the process data. Options available:

Manual Input: Directly enter the process attributes.
Random Generation: Automatically generate processes based on specified attributes and ranges.

## Simulation

After entering the input:

Verify the data, especially ensuring a time slice is defined if Round Robin is selected.
Choose one or more scheduling algorithms for simulation.
View the Gantt chart for detailed scheduling visualization.
Analyze turnaround and waiting times through tables and bar plots.
Compare overall performance with aggregated visual data across selected algorithms.

## Visualisation

Per-Process Metrics: Displays individual turnaround and waiting times.
Algorithm Comparison: Compares total and mean metrics across algorithms to identify the most efficient ones.

## Testing
The program includes a test.py file where you can input from files and validate the correctness of the scheduling simulations.

## Authors
Arnaoui Basma
Bouhadi Omar AlFarouq
