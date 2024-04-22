from flask import Flask, render_template, request
import random

app = Flask(__name__)

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

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/generate', methods=['GET', 'POST'])  # Renamed the route
def generate_random():
    if request.method == 'POST':
        num_processes = int(request.form['num_processes'])
        arrival_range = request.form['arrival_time_range']
        burst_range = request.form['burst_time_range']
        priority_range = request.form['priority_range'] if 'priority_range' in request.form else None
        processes = generate_random_processes(num_processes, arrival_range, burst_range, priority_range)
        return render_template('generated_processes.html', processes=processes)
    return render_template('generate.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/enter', methods=['GET', 'POST'])  # Allow both GET and POST requests
def enter():
    if request.method == 'POST':
        num_processes = int(request.form['num_processes'])
        return render_template('enter.html', num_processes=num_processes)
    return render_template('enter.html')


if __name__ == '__main__':
    app.run(debug=True)
