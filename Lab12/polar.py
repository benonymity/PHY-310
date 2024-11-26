import numpy as np
import matplotlib.pyplot as plt

# Create theta values from 0 to 2pi
theta = np.linspace(0, 2*np.pi, 100)

# Create x values
x = np.linspace(0, 15, 50)

# Create meshgrid for theta and x
THETA, X = np.meshgrid(theta, x)

# Calculate r values for each combination of theta and x
R = np.sqrt((np.cos(X)**4 + np.sin(X)**4 + 2*np.sin(X)**2*np.cos(X)**2*np.cos(THETA))**2 + 
            (2*np.cos(X)**2*np.sin(X)**2*(1-np.cos(THETA)))**2)

# Create the polar plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='polar')

# Create heatmap
heatmap = ax.pcolormesh(THETA, X, R, cmap='viridis')
plt.colorbar(heatmap)

plt.title('Polar Heatmap')
plt.show()
