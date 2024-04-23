from flask import Flask, render_template, request, session, redirect, url_for
import random

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
    if num_processes is None:
        return redirect(url_for('enter'))
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
        return render_template('entered_processes.html', processes=processes)
    return render_template('enter_details.html', num_processes=num_processes, priority_applicable=priority_applicable)


if __name__ == '__main__':
    app.run(debug=True)
