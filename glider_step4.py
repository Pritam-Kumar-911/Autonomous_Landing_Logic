# Step 4: 50 random flights
# Same brain as Step 3, but now every flight is different:
# random start height, random start position, random wind, and random gusts.
# Run with:  python glider_step4.py

import random
import csv
import matplotlib.pyplot as plt

# ----- Settings you can change -----
runs = 50             # how many flights to test
forward_speed = 15.0  # glider speed through the air (m/s)
target = 1000.0       # where we want to land (meters)
time_step = 0.1       # update every 0.1 seconds
gust = 8.0            # random gust strength (m/s) - try 4.0 for rough air
max_wind = 4.0        # steady wind is chosen between -max_wind and +max_wind

# ----- Brain settings (same as Step 3) -----
min_sink = 0.3
max_sink = 5.0
flare_height = 8.0
flare_tau = 2.0
flare_min_sink = 0.2
flare_time = 8.0

# ----- Success rules -----
max_miss = 30.0
max_touch_sink = 0.5

# Using the same seed makes the "random" flights repeat exactly.
# This way your results are the same every time you run it.
random.seed(42)


def fly(distance, height, wind):
    """Fly one landing. Returns where it landed, how hard, and the path."""
    stage = "APPROACH"
    sink_speed = 0.0
    xs = []
    hs = []

    while height > 0:
        # Ground speed = our speed + steady wind + a random gust
        ground_speed = forward_speed + wind + random.uniform(-gust, gust)

        if height <= flare_height:
            stage = "FLARE"

        if stage == "APPROACH":
            aim_point = target - ground_speed * flare_time
            distance_left = aim_point - distance
            if distance_left < 1:
                distance_left = 1
            time_left = distance_left / ground_speed
            sink_speed = (height - flare_height) / time_left
            if sink_speed < min_sink:
                sink_speed = min_sink
            if sink_speed > max_sink:
                sink_speed = max_sink
        else:
            sink_speed = height / flare_tau
            if sink_speed < flare_min_sink:
                sink_speed = flare_min_sink

        distance = distance + ground_speed * time_step
        height = height - sink_speed * time_step
        xs.append(distance)
        hs.append(max(height, 0))

    return distance, sink_speed, xs, hs


# ----- Run all the flights -----
results = []
paths = []

for number in range(1, runs + 1):
    start_distance = random.uniform(0, 200)   # random start position
    start_height = random.uniform(80, 150)    # random start height
    wind = random.uniform(-max_wind, max_wind)  # random steady wind

    landed, sink, xs, hs = fly(start_distance, start_height, wind)
    miss = landed - target
    good = abs(miss) <= max_miss and sink <= max_touch_sink

    results.append([number, round(start_distance), round(start_height),
                    round(wind, 1), round(miss, 1), round(sink, 2),
                    "PASS" if good else "FAIL"])
    paths.append((xs, hs, good))

# ----- Print the results table -----
print("run  start_x  start_h   wind   miss(m)  sink(m/s)  result")
for r in results:
    print(f"{r[0]:>3} {r[1]:>8} {r[2]:>8} {r[3]:>6} {r[4]:>9} {r[5]:>9}  {r[6]}")

passed = sum(1 for r in results if r[6] == "PASS")
average_miss = sum(abs(r[4]) for r in results) / runs
average_sink = sum(r[5] for r in results) / runs
print()
print("Success rate:", passed, "out of", runs, "=", round(100 * passed / runs), "%")
print("Average miss distance:", round(average_miss, 1), "m")
print("Average touchdown sink speed:", round(average_sink, 2), "m/s")

# ----- Save the table so you can show it to the judges -----
with open("results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["run", "start_x", "start_h", "wind", "miss_m", "sink_ms", "result"])
    writer.writerows(results)

# ----- Graph: all 50 flights together -----
for xs, hs, good in paths:
    plt.plot(xs, hs, color="tab:blue" if good else "tab:red", alpha=0.5)
plt.axvline(target, color="green", linestyle="--", label="Target")
plt.plot([], [], color="tab:blue", label="PASS")
plt.plot([], [], color="tab:red", label="FAIL")
plt.xlabel("Distance (m)")
plt.ylabel("Height (m)")
plt.title(f"Step 4: {runs} random flights - {passed} passed")
plt.legend()
plt.grid(True)
plt.savefig("glider_step4.png")
plt.show()