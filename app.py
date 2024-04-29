from flask import Flask, render_template, request, session, redirect, url_for
import random
from process import Process
from scheduler import Scheduler
import utils
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
            arrival_time = request.form[f'arrival_time_{i}']
            burst_time = request.form[f'burst_time_{i}']
            priority = request.form.get(f'priority_{i}') if priority_applicable else "N/A"

            processes.append({
                'arrival_time': arrival_time,
                'burst_time': burst_time,
                'priority': priority
            })
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
            arrival_time = int(process_data['arrival_time'])
            burst_time = int(process_data['burst_time'])
            priority = int(process_data['priority']) if priority_applicable else "N/A"
            processes.append(Process(i + 1, arrival_time, burst_time, priority))

        # Create a scheduler with the entered processes
        scheduler = Scheduler(processes)

        # Run FCFS algorithm
        scheduler.run_FCFS()

        # Store FCFS algorithm results
        fcfs_results = {
            'avg_turnaround_time': utils.calculate_average_turnaround_time(processes),
            'avg_waiting_time': utils.calculate_average_waiting_time(processes),
            'total_turnaround_time': utils.calculate_total_turnaround_time(processes),
            'total_waiting_time': utils.calculate_total_waiting_time(processes),
        }

    # Pass the entered processes, selected algorithms, and FCFS algorithm results to the template
    return render_template('entered_processes.html', processes=processes, selected_algorithms=selected_algorithms, fcfs_results=fcfs_results)


if __name__ == '__main__':
    app.run(debug=True)
