# Import necessary libraries
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import CheckButtons
from scipy.optimize import curve_fit

# Read data from file
with open('data.txt', 'r') as file:
    content = file.readlines()

# Find the start of each run in the data file
run_starts = [i for i, line in enumerate(content) if line.strip() == 'Vernier Format 2']

# Initialize lists to store data for all runs
all_runs_time = []
all_runs_position = []
all_runs_envelope = []
all_runs_oscillate = []
all_runs_envelope_equations = []
all_runs_oscillate_equations = []

# Define exponential decay function for envelope fitting
def exp_decay(t, A, tau, C):
    return A * np.exp(-t / tau) + C

# Define damped oscillation function for oscillation fitting
def oscillation(t, A, tau, C, w, p):
    return A * np.exp(-t / tau) * np.cos(w * t + p) + C

# Process each run
for i in range(len(run_starts)):
    # Extract data for current run
    start = run_starts[i] + 8
    end = (run_starts[i+1] - 7) if i+1 < len(run_starts) else len(content)
    run_data = np.loadtxt(content[start:end], usecols=(0, 1))
    
    # Remove first and last few data points if not the last run
    if i < len(run_starts) - 1:
        run_data = run_data[7:-6]
    else:
        run_data = run_data[7:]
    
    # Normalize position data
    center_line = np.mean(run_data[:, 1])
    normalized_position = run_data[:, 1] - center_line
    
    # Find peaks in the normalized position data
    peaks = []
    for j in range(1, len(normalized_position) - 1):
        if abs(normalized_position[j]) > abs(normalized_position[j-1]) and abs(normalized_position[j]) > abs(normalized_position[j+1]):
            peaks.append(j)
    
    peak_times = run_data[peaks, 0]
    peak_positions = np.abs(normalized_position[peaks])
    
    # Fit oscillation function to data
    try:
        popt_osc, _ = curve_fit(oscillation, run_data[:, 0], normalized_position, p0=[np.max(np.abs(normalized_position)), 1, 0, 2*np.pi, 0], maxfev=10000)
        A_osc, tau_osc, C_osc, w, p = popt_osc
        w = abs(w)  # Ensure positive frequency
    except RuntimeError:
        print(f"Warning: Optimal parameters not found for oscillation in run {i+1}. Using initial guesses.")
        A_osc, tau_osc, C_osc, w, p = np.max(peak_positions), 1, 0, 2*np.pi, 0
    
    # Fit envelope function to peak data
    try:
        popt_env, _ = curve_fit(exp_decay, peak_times, peak_positions, p0=[np.max(peak_positions), 1, 0], maxfev=10000)
        A_env, tau_env, C_env = popt_env
    except RuntimeError:
        print(f"Warning: Optimal parameters not found for envelope in run {i+1}. Using initial guesses.")
        A_env, tau_env, C_env = np.max(peak_positions), 1, 0
    
    # Generate fitted curves
    envelope = exp_decay(run_data[:, 0], A_env, tau_env, C_env)
    oscillate = oscillation(run_data[:, 0], A_osc, tau_osc, C_osc, w, p)
    
    # Store results for this run
    all_runs_time.append(run_data[:, 0])
    all_runs_position.append(normalized_position)
    all_runs_envelope.append(envelope)
    all_runs_oscillate.append(oscillate)
    all_runs_envelope_equations.append(f"$y = {A_env:.5f} e^{{\\frac{{-t}}{{{tau_env:.5f}}}}} + {C_env:.5f}$")
    all_runs_oscillate_equations.append(f"$y = {A_osc:.5f} e^{{\\frac{{-t}}{{{tau_osc:.5f}}}}} \cos({w:.5f}t + {p:.5f}) + {C_osc:.5f}$")

# Create main figure with all runs
fig, ax = plt.subplots(figsize=(10, 6))
lines = []
envelope_lines = []
oscillate_lines = []
equation_texts = []

# Plot data, envelope, and oscillation for each run
for i in range(len(all_runs_time)):
    line, = ax.plot(all_runs_time[i], all_runs_position[i])
    env_line, = ax.plot(all_runs_time[i], all_runs_envelope[i], '--', color=line.get_color(), alpha=0.5)
    osc_line, = ax.plot(all_runs_time[i], all_runs_oscillate[i], ':', color=line.get_color(), alpha=0.5)
    lines.append(line)
    envelope_lines.append(env_line)
    oscillate_lines.append(osc_line)
    
    # Add equation text for each run
    eq_text = ax.text(0.05, 0.95 - i*0.1, all_runs_envelope_equations[i] + '\n' + all_runs_oscillate_equations[i], 
                      transform=ax.transAxes, fontsize=8, verticalalignment='top', 
                      bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    equation_texts.append(eq_text)

# Set labels and grid
ax.set_xlabel('Time (s)')
ax.set_ylabel('Normalized Position (m)')
ax.grid(True)
ax.axhline(y=0, color='r', linestyle='--', label='Center Line')

# Create checkbuttons for toggling visibility
rax = plt.axes([0.85, 0.02, 0.12, 0.25])
labels = [f'{(i+1)*2} cm Disc' for i in range(len(all_runs_time))] + ['Envelope', 'Oscillation']
visibility = [True] * len(lines) + [True, True]
check = CheckButtons(rax, labels, visibility)

# Define function to handle checkbox clicks
def func(label):
    if label == 'Envelope':
        env_visible = not envelope_lines[0].get_visible()
        for env_line in envelope_lines:
            env_line.set_visible(env_visible)
        update_equation_visibility()
    elif label == 'Oscillation':
        osc_visible = not oscillate_lines[0].get_visible()
        for osc_line in oscillate_lines:
            osc_line.set_visible(osc_visible)
        update_equation_visibility()
    else:
        index = labels.index(label)
        lines[index].set_visible(not lines[index].get_visible())
        envelope_lines[index].set_visible(lines[index].get_visible() and check.get_status()[labels.index('Envelope')])
        oscillate_lines[index].set_visible(lines[index].get_visible() and check.get_status()[labels.index('Oscillation')])
        update_equation_visibility()
    plt.draw()

# Define function to update equation visibility
def update_equation_visibility():
    env_visible = check.get_status()[labels.index('Envelope')]
    osc_visible = check.get_status()[labels.index('Oscillation')]
    for i, eq_text in enumerate(equation_texts):
        if lines[i].get_visible():
            eq_parts = eq_text.get_text().split('\n')
            visible_parts = []
            if env_visible:
                visible_parts.append(eq_parts[0])
            if osc_visible:
                visible_parts.append(eq_parts[1])
            eq_text.set_text('\n'.join(visible_parts))
            eq_text.set_visible(bool(visible_parts))
        else:
            eq_text.set_visible(False)

# Connect checkbox click event to function
check.on_clicked(func)

# Print equations for each run
for i, eq in enumerate(all_runs_envelope_equations):
    print(f"Run {i+1} envelope equation: {eq}")
    print(f"Run {i+1} oscillation equation: {all_runs_oscillate_equations[i]}")

# Export individual graphs for each run
colors = ['green', 'orange', 'blue', 'red', 'purple']
for i in range(len(all_runs_time)):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    color = colors[i % len(colors)]
    
    # Plot data, envelope, and oscillation
    ax.plot(all_runs_time[i], all_runs_position[i], label=f'Run {i+1}', color=color)
    ax.plot(all_runs_time[i], all_runs_envelope[i], '--', alpha=0.5, label='Envelope', color=color)
    ax.plot(all_runs_time[i], all_runs_oscillate[i], ':', alpha=0.5, label='Oscillation', color=color)
    
    # Set labels and grid
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Normalized Position (m)')
    ax.grid(True)
    ax.axhline(y=0, color='r', linestyle='--', label='Center Line')
    
    # Add equation text
    ax.text(0.05, 0.95, f"Envelope: {all_runs_envelope_equations[i]}\nOscillation: {all_runs_oscillate_equations[i]}", 
            transform=ax.transAxes, fontsize=8, verticalalignment='top', 
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    
    ax.legend()
    
    # Save the figure
    plt.savefig(f'images/{(i+1)*2}cm.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

# Create an overlay of all runs
fig, ax = plt.subplots(figsize=(10, 6))

# Plot data, envelope, and oscillation for each run
for i in range(len(all_runs_time)):
    color = colors[i % len(colors)]
    ax.plot(all_runs_time[i], all_runs_position[i], label=f'{(i+1)*2} cm Disc', color=color)
    ax.plot(all_runs_time[i], all_runs_envelope[i], '--', alpha=0.5, color=color)
    ax.plot(all_runs_time[i], all_runs_oscillate[i], ':', alpha=0.5, color=color)

# Set labels, grid, and legend
ax.set_xlabel('Time (s)')
ax.set_ylabel('Normalized Position (m)')
ax.grid(True)
ax.axhline(y=0, color='r', linestyle='--', label='Center Line')
ax.legend()

# Save the overlay figure
plt.savefig('images/all_runs_overlay.png', dpi=300, bbox_inches='tight')
plt.close(fig)

# Display all figures
plt.show()
