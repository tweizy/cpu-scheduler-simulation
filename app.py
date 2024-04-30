from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import random
from process import Process
from scheduler import Scheduler
import utils
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

@app.route('/')
def menu():
    return render_template('menu.html')

def generate_random_processes(num_processes, arrival_range, burst_range, priority_range=None):
    processes = []
    for i in range(num_processes):
        arrival_time = random.randint(*map(int, arrival_range.split(',')))
        burst_time = random.randint(*map(int, burst_range.split(',')))
        priority = random.randint(*map(int, priority_range.split(','))) if priority_range else None
        process = {
            'process_id' : i+1,
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
        priority_range = request.form.get('priority_range')
        selected_algorithms = request.form.getlist('algorithm[]')
        if request.form.get('time_slice'):
            time_slice = int(request.form.get('time_slice', 5))
        else:
            time_slice = 5
        print("ha time")
        print(time_slice)
        # Generate random processes
        processes = generate_random_processes(num_processes, arrival_range, burst_range, priority_range)

        # Store form data in the session
        session['entered_processes_data'] = {
            'processes': processes,
            'arrival_range': arrival_range,
            'burst_range': burst_range,
            'priority_range': priority_range,
            'selected_algorithms': selected_algorithms,
            'time_slice': time_slice
        }
        print(session)
        # Redirect to the route for displaying generated processes
        return redirect(url_for('entered_processes'))  # Redirect to the entered_processes route

    return render_template('generate.html')


@app.route('/generated_processes')
def display_generated_processes():
    generated_processes_data = session.get('generated_processes_data', {})
    return render_template('generated_processes.html', data=generated_processes_data)


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
    selected_algorithms = request.form.getlist('algorithm[]')
    time_slice = int(request.form.get('time_slice', 5))

    # Retrieve selected algorithms from the form
    if num_processes is None:
        return redirect(url_for('enter'))
    print(request.method)
    if request.method == 'POST':
        processes = []
        for i in range(num_processes):
            arrival_time = request.form[f'arrival_time_{i}']

            burst_time = request.form[f'burst_time_{i}']
            priority = request.form.get(f'priority_{i}') if priority_applicable else None

            processes.append(Process(i+1,arrival_time,burst_time,priority))
        processes = [process.to_dict() for process in processes]

        # Sort processes by ID
        processes = sorted(processes, key=lambda x: int(x['process_id']))
        # Store form data in the session
        session['entered_processes_data'] = {
            'time_slice'  : time_slice,
            'processes': processes,
            'selected_algorithms': selected_algorithms
        }
        print("omaaar")
        print(time_slice)
        return redirect(url_for('entered_processes'))  # Redirect to the entered_processes route
    else:
        print("basma")
        return render_template('enter_details.html', num_processes=num_processes, priority_applicable=priority_applicable, time_slice = time_slice)




@app.route('/entered_processes', methods=['POST','GET'])
def entered_processes():
    # Retrieve entered details from the session
    entered_processes_data = session.get('entered_processes_data')
    time_slice = entered_processes_data['time_slice']
    print("yjfhgkkj")
    print(time_slice)
    if entered_processes_data is None:
        # Handle case where session data is missing or invalid
        return redirect(url_for('enter'))

    processes = entered_processes_data['processes']
    len_processes = len(processes)
    selected_algorithms = entered_processes_data['selected_algorithms']

    # Get priority applicability from session
    priority_applicable = session.get('priority_applicable')

    # Initialize variables to store FCFS results
    fcfs_results = None
    processes = []
    for i, process_data in enumerate(entered_processes_data['processes']):
        id = int(process_data['process_id'])
        arrival_time = int(process_data['arrival_time'])
        burst_time = int(process_data['burst_time'])
        priority = int(process_data['priority']) if priority_applicable else "N/A"
        processes.append(Process(id, arrival_time, burst_time, priority))
    # Create a scheduler with the entered processes
    scheduler = Scheduler(processes)
    fcfs_results = []
    sjf_results = []
    priority_results = []
    execution_data = []
    rr_results = []
    # Check if FCFS algorithm is selected
    if 'FCFS' in selected_algorithms:
        # Run FCFS algorithm
        gantt = scheduler.run_FCFS()
        scheduler.processes = processes
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
            'avg_turnaround_time': utils.calculate_average_turnaround_time(scheduler.processes),
            'avg_waiting_time': utils.calculate_average_waiting_time(scheduler.processes),
            'total_turnaround_time': utils.calculate_total_turnaround_time(scheduler.processes),
            'total_waiting_time': utils.calculate_total_waiting_time(scheduler.processes),
        }

        # Define a colormap
        cmap = plt.get_cmap('tab10')  # You can choose any colormap here

        # Create a dictionary to store process colors
        process_colors = {}

        # Plot Gantt chart for FCFS
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot each process on the Gantt chart
        for i, ed in enumerate(execution_data, start=1):
            start_time = ed['start_time']
            end_time = ed['end_time']
            duration = end_time - start_time

            # Assign a color to the process based on its ID
            color = cmap(i % 10)  # Limiting to 10 colors for simplicity, adjust as needed

            ax.barh(i, duration, left=start_time, height=0.4, align='center', color=color)

            # Annotate the bars with process IDs
            ax.text(start_time + duration / 2, i, f'Process {ed["process_id"]}', ha='center', va='center')

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

        # Save the figure to a file
        plt.savefig('static/gantt_chart1.png')

        # Calculate waiting time and turnaround time for each process
        waiting_times = []
        turnaround_times = []
        for i in range(len(processes)):
            process = utils.find_process_by_id(i+1,scheduler.processes)
            waiting_time = process.waiting
            turnaround_time = process.turnaround
            waiting_times.append(waiting_time)
            turnaround_times.append(turnaround_time)

        # Plot bar plot for waiting time
        plt.figure(figsize=(8, 6))
        plt.bar(range(1, len(waiting_times) + 1), waiting_times, color='skyblue')
        plt.xlabel('Process ID')
        plt.ylabel('Waiting Time')
        plt.title('Waiting Time for Each Process (FCFS)')
        plt.xticks(range(1, len(waiting_times) + 1))
        plt.savefig('static/waiting_time_fcfs.png')

        # Plot bar plot for turnaround time
        plt.figure(figsize=(8, 6))
        plt.bar(range(1, len(turnaround_times) + 1), turnaround_times, color='lightgreen')
        plt.xlabel('Process ID')
        plt.ylabel('Turnaround Time')
        plt.title('Turnaround Time for Each Process (FCFS)')
        plt.xticks(range(1, len(turnaround_times) + 1))
        plt.savefig('static/turnaround_time_fcfs.png')
        plt.close('all')

    if 'SJF' in selected_algorithms:
        # Run SJF algorithm
        gantt = scheduler.run_SJF()

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

        # Store SJF algorithm results
        sjf_results = {
            'avg_turnaround_time': utils.calculate_average_turnaround_time(scheduler.processes),
            'avg_waiting_time': utils.calculate_average_waiting_time(scheduler.processes),
            'total_turnaround_time': utils.calculate_total_turnaround_time(scheduler.processes),
            'total_waiting_time': utils.calculate_total_waiting_time(scheduler.processes),
        }

        # Calculate waiting time and turnaround time for each process
        waiting_times = []
        turnaround_times = []
        current_time = 0
        for i in range(len(processes)):
            process = utils.find_process_by_id(i+1, scheduler.processes)
            turnaround_time = process.turnaround
            waiting_time = process.waiting
            waiting_times.append(waiting_time)
            turnaround_times.append(turnaround_time)

        # Plot Gantt chart
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_ylim(0.5, len(execution_data) + 0.5)
        ax.set_xlim(0, max(ed['end_time'] for ed in execution_data))
        ax.set_xlabel('Time')
        ax.set_ylabel('Processes')
        ax.set_yticks(range(1, len(execution_data) + 1))
        ax.set_yticklabels([f'Process {ed["process_id"]}' for ed in execution_data])
        ax.xaxis.set_major_locator(plt.MultipleLocator(1))

        def format_x_ticks(x, pos=None):
            return f'{int(x):d}'

        ax.xaxis.set_major_formatter(plt.FuncFormatter(format_x_ticks))
        ax.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)
        cmap = plt.get_cmap('tab10')
        for i, ed in enumerate(execution_data, start=1):
            start_time = ed['start_time']
            end_time = ed['end_time']
            duration = end_time - start_time
            color = cmap(i % 10)
            ax.barh(i, duration, left=start_time, height=0.4, align='center', color=color)
            ax.text(start_time + duration / 2, i, f'Process {ed["process_id"]}', ha='center', va='center')
        plt.savefig('static/gantt_chart2.png')

        waiting_times = []
        turnaround_times = []
        print("kleeeeen")
        print(len(processes))
        processes = scheduler.processes
        for i in range(len(processes)):
            process = utils.find_process_by_id(i + 1, scheduler.processes)
            waiting_time = process.waiting
            turnaround_time = process.turnaround
            waiting_times.append(waiting_time)
            turnaround_times.append(turnaround_time)

        # Plot bar plot for waiting time
        plt.figure(figsize=(8, 6))
        plt.bar(range(1, len(waiting_times) + 1), waiting_times, color='skyblue')
        plt.xlabel('Process ID')
        plt.ylabel('Waiting Time')
        plt.title('Waiting Time for Each Process (SJF)')
        plt.xticks(range(1, len(waiting_times) + 1))
        plt.savefig('static/waiting_time_sjf.png')

        # Plot bar plot for turnaround time
        plt.figure(figsize=(8, 6))
        plt.bar(range(1, len(turnaround_times) + 1), turnaround_times, color='lightgreen')
        plt.xlabel('Process ID')
        plt.ylabel('Turnaround Time')
        plt.title('Turnaround Time for Each Process (SJF)')
        plt.xticks(range(1, len(turnaround_times) + 1))
        plt.savefig('static/turnaround_time_sjf.png')
        plt.close('all')

    if 'Priority' in selected_algorithms:
        # Run Priority Scheduling algorithm
        gantt = scheduler.run_priority_scheduling()

        execution_data = []

        # Process the gantt data to create execution intervals
        current_time = 0
        for process_id, burst_time in gantt:
            start_time = current_time
            end_time = current_time + burst_time
            execution_data.append({'process_id': process_id, 'start_time': start_time, 'end_time': end_time})
            current_time = end_time

        # Sort execution_data by process IDs
        execution_data.sort(key=lambda x: x['process_id'])

        # Store Priority Scheduling algorithm results
        priority_results = {
            'avg_turnaround_time': utils.calculate_average_turnaround_time(scheduler.processes),
            'avg_waiting_time': utils.calculate_average_waiting_time(scheduler.processes),
            'total_turnaround_time': utils.calculate_total_turnaround_time(scheduler.processes),
            'total_waiting_time': utils.calculate_total_waiting_time(scheduler.processes),
        }

        # Calculate waiting time and turnaround time for each process
        waiting_times = []
        turnaround_times = []
        for i in range(len(scheduler.processes)):
            process = utils.find_process_by_id(i+1, scheduler.processes)
            waiting_time = process.waiting
            turnaround_time = process.turnaround
            waiting_times.append(waiting_time)
            turnaround_times.append(turnaround_time)

        # Plot Gantt chart
        fig, ax = plt.subplots(figsize=(10, 6))

        # Set up the axes formatting
        ax.set_ylim(0.5, len(execution_data) + 0.5)
        ax.set_xlim(0, max(ed['end_time'] for ed in execution_data))
        ax.set_xlabel('Time')
        ax.set_ylabel('Processes')
        ax.set_yticks(range(1, len(execution_data) + 1))
        ax.set_yticklabels([f'Process {ed["process_id"]}' for ed in execution_data])
        ax.xaxis.set_major_locator(plt.MultipleLocator(1))

        def format_x_ticks(x, pos=None):
            return f'{int(x):d}'

        ax.xaxis.set_major_formatter(plt.FuncFormatter(format_x_ticks))
        ax.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)
        cmap = plt.get_cmap('tab10')
        for i, ed in enumerate(execution_data, start=1):
            start_time = ed['start_time']
            end_time = ed['end_time']
            duration = end_time - start_time
            color = cmap(i % 10)
            ax.barh(i, duration, left=start_time, height=0.4, align='center', color=color)
            ax.text(start_time + duration / 2, i, f'Process {ed["process_id"]}', ha='center', va='center')
        plt.savefig('static/gantt_chart3.png')

        # Plot bar plot for waiting time
        plt.figure(figsize=(8, 6))
        plt.bar(range(1, len(waiting_times) + 1), waiting_times, color='skyblue')
        plt.xlabel('Process ID')
        plt.ylabel('Waiting Time')
        plt.title('Waiting Time for Each Process (Priority Scheduling)')
        plt.xticks(range(1, len(waiting_times) + 1))
        plt.savefig('static/waiting_time_priority.png')

        # Plot bar plot for turnaround time
        plt.figure(figsize=(8, 6))
        plt.bar(range(1, len(turnaround_times) + 1), turnaround_times, color='lightgreen')
        plt.xlabel('Process ID')
        plt.ylabel('Turnaround Time')
        plt.title('Turnaround Time for Each Process (Priority Scheduling)')
        plt.xticks(range(1, len(turnaround_times) + 1))
        plt.savefig('static/turnaround_time_priority.png')

    if 'RR' in selected_algorithms:
        # Run Round Robin algorithm
        gantt = scheduler.run_round_robin(time_slice)

        execution_data = []

        # Process the gantt data to create execution intervals
        current_time = 0

        for process_id, run_time in gantt:
            start_time = current_time
            end_time = current_time + run_time
            execution_data.append({'process_id': process_id, 'start_time': start_time, 'end_time': end_time})
            current_time = end_time

        # Sort execution_data by process IDs
        execution_data.sort(key=lambda x: x['process_id'])

        # Store Round Robin algorithm results
        rr_results = {
            'avg_turnaround_time': utils.calculate_average_turnaround_time(scheduler.processes),
            'avg_waiting_time': utils.calculate_average_waiting_time(scheduler.processes),
            'total_turnaround_time': utils.calculate_total_turnaround_time(scheduler.processes),
            'total_waiting_time': utils.calculate_total_waiting_time(scheduler.processes),
        }

        # Calculate waiting time and turnaround time for each process
        waiting_times = []
        turnaround_times = []
        for i in range(len(scheduler.processes)):
            process = utils.find_process_by_id(i+1, scheduler.processes)
            waiting_time = process.waiting
            turnaround_time = process.turnaround
            waiting_times.append(waiting_time)
            turnaround_times.append(turnaround_time)

        # Define a colormap
        cmap = plt.get_cmap('tab10')  # You can choose any colormap here

        # Create a dictionary to store process colors
        process_colors = {}

        # Plot Gantt chart for Round Robin
        fig, ax = plt.subplots(figsize=(10, 6))

        # Set up the axes formatting
        ax.set_ylim(0.5, len(execution_data) + 0.5)
        ax.set_xlim(0, max(ed['end_time'] for ed in execution_data))
        ax.set_xlabel('Time')
        ax.set_ylabel('Processes')
        ax.set_yticks(range(1, len(execution_data) + 1))
        ax.set_yticklabels([f'Process {ed["process_id"]}' for ed in execution_data])
        ax.xaxis.set_major_locator(plt.MultipleLocator(1))

        def format_x_ticks(x, pos=None):
            return f'{int(x):d}'

        ax.xaxis.set_major_formatter(plt.FuncFormatter(format_x_ticks))
        ax.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)

        # Plot each process on the Gantt chart
        for i, ed in enumerate(execution_data, start=1):
            start_time = ed['start_time']
            end_time = ed['end_time']
            duration = end_time - start_time

            process_id = ed["process_id"]

            # Assign color to process if not assigned yet
            if process_id not in process_colors:
                process_colors[process_id] = cmap(len(process_colors) % 10)

            color = process_colors[process_id]

            ax.barh(i, duration, left=start_time, height=0.4, align='center', color=color)
            ax.text(start_time + duration / 2, i, f'Process {process_id}', ha='center', va='center')

            # Set x-axis limits based on the start and end times
            ax.set_xlim(0, max(ed['end_time'] for ed in execution_data))

        # Save the figure to a file
        plt.savefig('static/gantt_chart4.png')

        # Plot bar plot for waiting time
        plt.figure(figsize=(8, 6))
        plt.bar(range(1, len(waiting_times) + 1), waiting_times, color='skyblue')
        plt.xlabel('Process ID')
        plt.ylabel('Waiting Time')
        plt.title('Waiting Time for Each Process (Round Robin)')
        plt.xticks(range(1, len(waiting_times) + 1))
        plt.savefig('static/waiting_time_rr.png')

        # Plot bar plot for turnaround time
        plt.figure(figsize=(8, 6))
        plt.bar(range(1, len(turnaround_times) + 1), turnaround_times, color='lightgreen')
        plt.xlabel('Process ID')
        plt.ylabel('Turnaround Time')
        plt.title('Turnaround Time for Each Process (Round Robin)')
        plt.xticks(range(1, len(turnaround_times) + 1))
        plt.savefig('static/turnaround_time_rr.png')

    scheduler.processes.sort(key=lambda x: x.id)
    num_processes = len(scheduler.processes)
    # Pass the entered processes, selected algorithms, and FCFS algorithm results to the template
    return render_template('entered_processes.html', processes=scheduler.processes, selected_algorithms=selected_algorithms, sjf_results=sjf_results, fcfs_results=fcfs_results, execution_data=execution_data, num_processes = num_processes, priority_results = priority_results, rr_results = rr_results)

if __name__ == '__main__':
    app.run(debug=True)
