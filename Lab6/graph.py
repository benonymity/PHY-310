import matplotlib.pyplot as plt
import numpy as np
import csv
import os
from matplotlib.widgets import CheckButtons

def load_data(filename):
    data = {}
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        headers = next(csvreader)
        for i, header in enumerate(headers):
            if i > 0:  # Skip the time column
                data[header] = []
        data['Time (s)'] = []
        
        for row in csvreader:
            try:
                time = float(row[0])
                if time <= 1.0:  # Only load data for the first second
                    data['Time (s)'].append(time)
                    for i, value in enumerate(row[1:], start=1):
                        if value.strip():  # Check if the value is not empty
                            data[headers[i]].append(float(value))
                        else:
                            data[headers[i]].append(np.nan)  # Use NaN for empty values
                else:
                    break  # Stop reading after the first second
            except ValueError:
                print(f"Skipping row due to invalid data: {row}")
    
    return data

def plot_data():
    data_folder = 'data/'
    csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]
    
    for csv_file in csv_files:
        filename = os.path.join(data_folder, csv_file)
        data = load_data(filename)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        lines = []
        labels = []
        
        for key, values in data.items():
            if key != 'Time (s)':
                label = key
                line, = ax.plot(data['Time (s)'], values, label=label)
                lines.append(line)
                labels.append(label)
        
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Value')
        ax.set_title(f'Data from {csv_file} (First Second)')
        ax.legend()
        ax.set_xlim(0, 1)  # Set x-axis limit to 1 second
        
        plt.tight_layout()
        
        # Add checkboxes
        # plt.subplots_adjust(left=0.25)
        # ax_check = plt.axes([0.01, 0.3, 0.2, 0.6])
        # check = CheckButtons(ax_check, labels, [True] * len(labels))
        
        # def func(label):
        #     index = labels.index(label)
        #     lines[index].set_visible(not lines[index].get_visible())
        #     plt.draw()
        
        # check.on_clicked(func)
    
    plt.show()

if __name__ == "__main__":
    plot_data()
