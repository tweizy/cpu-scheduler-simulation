from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import random
from process import Process
from scheduler import Scheduler
import utils
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import timedelta

import json
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

@app.route('/')
def menu():
    return render_template('menu.html')

def generate_random_processes(num_processes, arrival_range, burst_range, priority_range=None):
    processes = []
    for _ in range(num_processes):
        arrival_time = random.randint(*map(int, arrival_range.split(',')))
        burst_time = random.randint(*map(int, burst_range.split(',')))
        priority = random.randint(*map(int, priority_range.split(','))) if priority_range else None
        process = {
            'arrival_time': arrival_time,
            'burst_time': burst_time,
        }
        if priority:
            process['priority'] = priority
        processes.append(process)
    return processes


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        num_processes = int(request.form['num_processes'])
        arrival_range = request.form['arrival_time_range']
        burst_range = request.form['burst_time_range']
        priority_range = request.form['priority_range'] if 'priority_range' in request.form else None
        processes = generate_random_processes(num_processes, arrival_range, burst_range, priority_range)
        return render_template('entered_processes.html', processes=processes)
    return render_template('generate.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/enter', methods=['GET', 'POST'])
def enter():
    if request.method == 'POST':
        num_processes = int(request.form['num_processes'])
        session['num_processes'] = num_processes
        session['priority_applicable'] = 'priority_applicable' in request.form
        return redirect(url_for('enter_details'))
    return render_template('enter.html')


@app.route('/enter_details', methods=['GET', 'POST'])
def enter_details():
    num_processes = session.get('num_processes')
    priority_applicable = session.get('priority_applicable')
    selected_algorithms = request.form.getlist('algorithm[]')  # Retrieve selected algorithms from the form
    if num_processes is None:
        return redirect(url_for('enter'))
    print(request.method)
    if request.method == 'POST':
        processes = []
        for i in range(num_processes):
            process_id = i+1
            arrival_time = request.form[f'arrival_time_{i}']
            burst_time = request.form[f'burst_time_{i}']
            priority = request.form.get(f'priority_{i}') if priority_applicable else "N/A"

            processes.append({
                'process_id' : process_id,
                'arrival_time': arrival_time,
                'burst_time': burst_time,
                'priority': priority
            })
            print(processes)
        # Store form data in the session
        session['entered_processes_data'] = {
            'processes': processes,
            'selected_algorithms': selected_algorithms
        }
        return redirect(url_for('entered_processes'))  # Redirect to the entered_processes route
    else:
        print("basma")
        return render_template('enter_details.html', num_processes=num_processes, priority_applicable=priority_applicable)




@app.route('/entered_processes', methods=['POST','GET'])
def entered_processes():
    # Retrieve entered details from the session
    entered_processes_data = session.get('entered_processes_data')
    if entered_processes_data is None:
        # Handle case where session data is missing or invalid
        return redirect(url_for('enter'))

    processes = entered_processes_data['processes']
    selected_algorithms = entered_processes_data['selected_algorithms']

    # Get priority applicability from session
    priority_applicable = session.get('priority_applicable')

    # Initialize variables to store FCFS results
    fcfs_results = None

    # Check if FCFS algorithm is selected
    if 'FCFS' in selected_algorithms:
        # Process the form data to create a list of Process objects
        processes = []
        for i, process_data in enumerate(entered_processes_data['processes']):
            id = int(process_data['process_id'])
            arrival_time = int(process_data['arrival_time'])
            burst_time = int(process_data['burst_time'])
            priority = int(process_data['priority']) if priority_applicable else "N/A"
            processes.append(Process(id, arrival_time, burst_time, priority))

        # Create a scheduler with the entered processes
        scheduler = Scheduler(processes)

        # Run FCFS algorithm
        gantt = scheduler.run_FCFS()
        execution_data = []

        # Process the gantt data to create execution intervals
        current_time = 0
        for process_id in gantt:
            start_time = current_time
            end_time = current_time + process_id[1]  # Assuming each process executes for 1 unit of time
            execution_data.append({'process_id': process_id[0], 'start_time': start_time, 'end_time': end_time})
            current_time = end_time

        # Sort execution_data by process IDs
        execution_data.sort(key=lambda x: x['process_id'])

        # Store FCFS algorithm results
        fcfs_results = {
            'avg_turnaround_time': utils.calculate_average_turnaround_time(processes),
            'avg_waiting_time': utils.calculate_average_waiting_time(processes),
            'total_turnaround_time': utils.calculate_total_turnaround_time(processes),
            'total_waiting_time': utils.calculate_total_waiting_time(processes),
        }
        print(execution_data)
        fig, ax = plt.subplots(figsize=(10, 6))

        # Set up the axes formatting
        ax.set_ylim(0.5, len(execution_data) + 0.5)
        ax.set_xlim(0, max(ed['end_time'] for ed in execution_data))
        ax.set_xlabel('Time')
        ax.set_ylabel('Processes')
        ax.set_yticks(range(1, len(execution_data) + 1))
        ax.set_yticklabels([f'Process {ed["process_id"]}' for ed in execution_data])

        # Change x-axis locator to integer increments
        ax.xaxis.set_major_locator(plt.MultipleLocator(1))

        # Format x-axis labels as integers without leading zeros
        def format_x_ticks(x, pos=None):
            return f'{int(x):d}'

        ax.xaxis.set_major_formatter(plt.FuncFormatter(format_x_ticks))

        # Set grid for better readability
        ax.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)

        # Plot each process on the Gantt chart
        # Plot each process on the Gantt chart
        # Plot each process on the Gantt chart
        for i, ed in enumerate(execution_data, start=1):
            start_time = ed['start_time']
            end_time = ed['end_time']
            duration = end_time - start_time
            ax.barh(i, duration, left=start_time, height=0.4, align='center')

            # Annotate the bars with process IDs
            ax.text(start_time + duration / 2, i, f'Process {ed["process_id"]}', ha='center', va='center')

            # Set x-axis limits based on the start and end times
            ax.set_xlim(0, max(ed['end_time'] for ed in execution_data))

        # Save the figure to a file
        plt.savefig('static/gantt_chart1.png')

    # Convert execution_data to JSON string
    execution_data_json = json.dumps(execution_data)


    # Pass the entered processes, selected algorithms, and FCFS algorithm results to the template
    return render_template('entered_processes.html', processes=processes, selected_algorithms=selected_algorithms, fcfs_results=fcfs_results, execution_data=execution_data_json)

if __name__ == '__main__':
    app.run(debug=True)
