import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import CheckButtons
from scipy.optimize import curve_fit

with open('data.txt', 'r') as file:
    content = file.readlines()

run_starts = [i for i, line in enumerate(content) if line.strip() == 'Vernier Format 2']

all_runs_time = []
all_runs_position = []
all_runs_envelope = []
all_runs_equations = []

def exp_decay(t, A, tau, C):
    return A * np.exp(-t / tau) + C

for i in range(len(run_starts)):
    start = run_starts[i] + 8
    end = (run_starts[i+1] - 7) if i+1 < len(run_starts) else len(content)
    
    run_data = np.loadtxt(content[start:end], usecols=(0, 1))
    
    if i < len(run_starts) - 1:
        run_data = run_data[7:-6]
    else:
        run_data = run_data[7:]
    
    center_line = np.mean(run_data[:, 1])
    normalized_position = run_data[:, 1] - center_line
    
    peaks = []
    for j in range(1, len(normalized_position) - 1):
        if abs(normalized_position[j]) > abs(normalized_position[j-1]) and abs(normalized_position[j]) > abs(normalized_position[j+1]):
            peaks.append(j)
    
    peak_times = run_data[peaks, 0]
    peak_positions = np.abs(normalized_position[peaks])
    
    popt, _ = curve_fit(exp_decay, peak_times, peak_positions, p0=[np.max(peak_positions), 1, 0])
    A, tau, C = popt
    
    envelope = exp_decay(run_data[:, 0], A, tau, C)
    
    all_runs_time.append(run_data[:, 0])
    all_runs_position.append(normalized_position)
    all_runs_envelope.append(envelope)
    all_runs_equations.append(f"y = {A:.4f} * exp(-t / {tau:.4f}) + {C:.4f}")

fig, ax = plt.subplots(figsize=(10, 6))
lines = []
envelope_lines = []
equation_texts = []
for i in range(len(all_runs_time)):
    line, = ax.plot(all_runs_time[i], all_runs_position[i])
    env_line, = ax.plot(all_runs_time[i], all_runs_envelope[i], '--', color=line.get_color(), alpha=0.5)
    lines.append(line)
    envelope_lines.append(env_line)
    
    # Add equation text
    eq_text = ax.text(0.05, 0.95 - i*0.05, all_runs_equations[i], transform=ax.transAxes, 
                      fontsize=8, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    equation_texts.append(eq_text)

ax.set_xlabel('Time (s)')
ax.set_ylabel('Normalized Position (m)')
ax.set_title('Oscillating Springs Damped by Discs')
ax.grid(True)
ax.axhline(y=0, color='r', linestyle='--', label='Center Line')

rax = plt.axes([0.85, 0.02, 0.12, 0.15])
labels = [f'{(i+1)*2} cm Disc' for i in range(len(all_runs_time))]
visibility = [True] * len(lines)
check = CheckButtons(rax, labels, visibility)

def func(label):
    index = labels.index(label)
    lines[index].set_visible(not lines[index].get_visible())
    envelope_lines[index].set_visible(lines[index].get_visible())
    equation_texts[index].set_visible(lines[index].get_visible())
    plt.draw()

check.on_clicked(func)

for i, eq in enumerate(all_runs_equations):
    print(f"Run {i+1} envelope equation: {eq}")


# Export individual graphs for each run
colors = ['green', 'orange', 'blue', 'red', 'purple']
for i in range(len(all_runs_time)):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Use predefined colors
    color = colors[i % len(colors)]
    
    ax.plot(all_runs_time[i], all_runs_position[i], label=f'Run {i+1}', color=color)
    ax.plot(all_runs_time[i], all_runs_envelope[i], '--', alpha=0.5, label='Envelope', color=color)
    
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Normalized Position (m)')
    # ax.set_title(f'Oscillating Spring Damped by a {(i+1)*2} cm Disc')
    ax.grid(True)
    ax.axhline(y=0, color='r', linestyle='--', label='Center Line')
    
    ax.text(0.05, 0.95, all_runs_equations[i], transform=ax.transAxes, 
            fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    
    # Save the figure
    plt.savefig(f'images/{(i+1)*2}cm.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

plt.show()
