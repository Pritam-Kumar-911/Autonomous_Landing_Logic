# Step 3: The flare (soft landing)
# Two stages now:
#   APPROACH: aim for a point a little BEFORE the target, arriving at flare height
#   FLARE:    near the ground, sink slower and slower so we touch down softly
# Run with:  python glider_step3.py

import matplotlib.pyplot as plt

# ----- Starting values (you can change these) -----
height = 120.0        # starting height in meters
distance = 0.0        # how far forward we have flown, in meters
forward_speed = 15.0  # glider speed through the air, meters per second
wind = 0.0            # + is a tailwind, - is a headwind
target = 1000.0       # where we want to land, in meters from the start
time_step = 0.1       # we update every 0.1 seconds

# ----- Approach limits -----
min_sink = 0.3
max_sink = 5.0

# ----- Flare settings -----
flare_height = 8.0    # start the flare below this height (meters)
flare_tau = 2.0       # bigger number = slower, gentler flare
flare_min_sink = 0.2  # never sink slower than this during the flare
flare_time = 8.0      # roughly how many seconds the flare takes

# ----- Success rules for the demo -----
max_miss = 30.0       # must land within this many meters of the target
max_touch_sink = 0.5  # must touch down slower than this (m/s)

# ----- Notebooks to remember the path -----
approach_x = []
approach_h = []
flare_x = []
flare_h = []

stage = "APPROACH"
sink_speed = 0.0

while height > 0:
    ground_speed = forward_speed + wind

    # Switch to the flare stage when we are low enough
    if height <= flare_height:
        stage = "FLARE"

    if stage == "APPROACH":
        # The flare will use up some distance, so aim BEFORE the target.
        aim_point = target - ground_speed * flare_time
        distance_left = aim_point - distance
        if distance_left < 1:
            distance_left = 1
        time_left = distance_left / ground_speed

        # Sink fast enough to arrive at flare height right at the aim point
        sink_speed = (height - flare_height) / time_left
        if sink_speed < min_sink:
            sink_speed = min_sink
        if sink_speed > max_sink:
            sink_speed = max_sink
    else:
        # FLARE: the lower we are, the slower we sink
        sink_speed = height / flare_tau
        if sink_speed < flare_min_sink:
            sink_speed = flare_min_sink

    # Move the glider
    distance = distance + ground_speed * time_step
    height = height - sink_speed * time_step

    # Save the position in the right notebook
    if stage == "APPROACH":
        approach_x.append(distance)
        approach_h.append(max(height, 0))
    else:
        flare_x.append(distance)
        flare_h.append(max(height, 0))

# ----- Results -----
miss = distance - target
good = abs(miss) <= max_miss and sink_speed <= max_touch_sink
print("Landed at", round(distance), "m. Target was", round(target), "m.")
print("Miss distance:", round(miss, 1), "m (negative = landed short)")
print("Sink speed at touchdown:", round(sink_speed, 2), "m/s")
print("RESULT:", "PASS" if good else "FAIL")

# ----- Graph -----
plt.plot(approach_x, approach_h, color="tab:blue", label="Approach")
plt.plot(flare_x, flare_h, color="tab:red", linewidth=3, label="Flare")
plt.axvline(target, color="green", linestyle="--", label="Target")
plt.xlabel("Distance (m)")
plt.ylabel("Height (m)")
plt.title("Step 3: Approach and flare")
plt.legend()
plt.grid(True)
plt.savefig("glider_step3.png")
plt.show()