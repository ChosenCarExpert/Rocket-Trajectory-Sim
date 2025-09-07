import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ------------------------
# SpaceX Falcon 9 Booster Approx Parameters Example
# Can be changed for different rockets
dry_mass = 230000.0        # kg
fuel_mass = 411000.0       # kg
burn_rate = 2200.0         # kg/s
thrust_force = 73500000.0  # N
g = 9.8                    # gravity (m/s^2)
dt = 0.1                   # time step (s)

# Initial state
y = 0.0
v = 0.0
t = 0.0

time = []
height = []


# Simulation loop
while y >= 0 and t < 7500:
    if fuel_mass > 0:
        fuel_mass -= burn_rate * dt
        if fuel_mass < 0:
            fuel_mass = 0

    current_mass = dry_mass + fuel_mass
    thrust = thrust_force if fuel_mass > 0 else 0
    weight = current_mass * g
    net_force = thrust - weight

    a = net_force / current_mass
    v += a * dt
    y += v * dt
    if y < 0:
        y = 0

    time.append(t)
    height.append(y)

    if int(t*10) % 10 == 0:  # every 1s
        print(f"t={t:.1f}s, mass={current_mass/1000:.1f}t, thrust={thrust/1000:.1f}kN, v={v:.2f}m/s, y={y/1000:.2f}km")

    t += dt

# ------------------------
# Results
max_height = max(height)
print(f"\nMax height: {max_height:.2f} m ({max_height/1000:.2f} km)")

# ------------------------
# Plot
plt.figure(figsize=(10,6))
plt.plot(time, [h/1000 for h in height], color="blue", linewidth=2)  # plot in km
plt.xlabel("Time (s)", fontsize=12)
plt.ylabel("Height (km)", fontsize=12)
plt.title("SpaceX Falcon 9 Booster Trajectory (Simplified)", fontsize=14)
plt.grid(True)

# format
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.show()
