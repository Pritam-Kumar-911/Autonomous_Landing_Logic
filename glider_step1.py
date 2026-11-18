# Step 1: The pretend glider
# A dot that flies forward and sinks down until it hits the ground.
# Run with:  python glider_step1.py
# Needs matplotlib:  pip install matplotlib

import matplotlib.pyplot as plt

# ----- Starting values (you can change these) -----
height = 100.0        # starting height in meters
distance = 0.0        # how far forward we have flown, in meters
forward_speed = 30.0  # meters per second
sink_speed = 1.5      # how fast we go down, meters per second
time_step = 0.01       # we update every 0.1 seconds

# ----- Lists to remember where the glider has been -----
distances = []
heights = []

# ----- The loop: repeat until the glider reaches the ground -----
while height > 0:
    # 1. Move forward a little
    distance = distance + forward_speed * time_step

    # 2. Go down a little
    height = height - sink_speed * time_step

    # 3. Save the position (never save a height below zero)
    distances.append(distance)
    heights.append(max(height, 0))

# ----- Print the result -----
print("The glider landed", round(distance), "meters from where it started.")

# ----- Draw the graph -----
plt.plot(distances, heights)
plt.xlabel("Distance (m)")
plt.ylabel("Height (m)")
plt.title("Step 1: Pretend glider")
plt.grid(True)
plt.savefig("glider_step1.png")
plt.show()