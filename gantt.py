# Create a figure and a single subplot
execution_data = {}
fig, ax = plt.subplots(figsize=(10, 6))

# Set up the axes formatting
ax.set_ylim(0.5, len(execution_data) + 0.5)
ax.set_xlim(0, max(ed['end_time'] for ed in execution_data))
ax.set_xlabel('Time')
ax.set_ylabel('Processes')
ax.set_yticks(range(1, len(execution_data) + 1))
ax.set_yticklabels([f'Process {ed["process_id"]}' for ed in execution_data])
ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

# Set grid for better readability
ax.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)

# Plot each process on the Gantt chart
for ed in execution_data:
    start_time = ed['start_time']
    end_time = ed['end_time']
    ax.barh(ed['process_id'], end_time - start_time, left=start_time, height=0.4, align='center')

# Save the figure to a file
plt.savefig('/mnt/data/gantt_chart.png')

# Display the plot
plt.show()