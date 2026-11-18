# Step 2: Give the glider a brain
# The glider now has a TARGET spot. Every 0.1 seconds the brain asks:
#   "How fast must I sink so I reach the ground exactly at the target?"
# Run with:  python glider_step2.py

import matplotlib.pyplot as plt

# ----- Starting values (you can change these) -----
height = 120.0        # starting height in meters
distance = 0.0        # how far forward we have flown, in meters
forward_speed = 15.0  # glider speed through the air, meters per second
wind = 0.0            # + is a tailwind (pushes us forward), - is a headwind
target = 1000.0       # where we want to land, in meters from the start
time_step = 0.1       # we update every 0.1 seconds

# ----- Brain limits: the glider cannot sink too slowly or too fast -----
min_sink = 0.3
max_sink = 5.0

# ----- Notebooks to remember the path -----
distances = []
heights = []

# ----- The loop -----
while height > 0:
    # How fast are we really moving over the ground? (wind helps or hurts)
    ground_speed = forward_speed + wind

    # BRAIN, step A: how far is the target from us right now?
    distance_left = target - distance
    if distance_left < 1:
        distance_left = 1          # avoid dividing by zero near the target

    # BRAIN, step B: how long until we reach the target at this speed?
    time_left = distance_left / ground_speed

    # BRAIN, step C: to touch the ground at that moment, we must sink this fast
    sink_speed = height / time_left

    # Keep the sink speed inside the allowed limits
    if sink_speed < min_sink:
        sink_speed = min_sink
    if sink_speed > max_sink:
        sink_speed = max_sink

    # Move the glider (same as Step 1)
    distance = distance + ground_speed * time_step
    height = height - sink_speed * time_step

    distances.append(distance)
    heights.append(max(height, 0))

# ----- Results -----
miss = distance - target
print("Landed at", round(distance), "m. Target was", round(target), "m.")
print("Miss distance:", round(miss, 1), "m (negative = landed short)")
print("Sink speed at touchdown:", round(sink_speed, 2), "m/s")

# ----- Graph -----
plt.plot(distances, heights, label="Glider path")
plt.axvline(target, color="green", linestyle="--", label="Target")
plt.xlabel("Distance (m)")
plt.ylabel("Height (m)")
plt.title("Step 2: Glider with a brain")
plt.legend()
plt.grid(True)
plt.savefig("glider_step2.png")
plt.show()