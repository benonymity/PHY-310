# Import necessary libraries
import numpy as np

# Read data from file
with open('data.txt', 'r') as file:
    content = file.readlines()

# Find the start of each run in the data file
run_starts = [i for i, line in enumerate(content) if line.strip() == 'Vernier Format 2']

# Initialize list to store standard deviations for all runs
all_runs_std = []

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
    
    # Calculate standard deviation
    std_dev = np.std(normalized_position)
    
    # Store result for this run
    all_runs_std.append(std_dev)

# Print standard deviations for each run
for i, std in enumerate(all_runs_std):
    print(f"Run {i+1} standard deviation: {std:.6f}")

# Calculate overall standard deviation
overall_std = np.sqrt(np.mean(np.array(all_runs_std)**2))
print(f"\nOverall standard deviation: {overall_std:.6f}")
