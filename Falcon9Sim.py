import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ------------------------
# Falcon 9 Parameters
# ------------------------
# Stage 1
stage1_dry = 30000.0       # kg
stage1_fuel = 411000.0     # kg
stage1_thrust = 7.35e6     # N
stage1_burn_time = 162     # seconds

# Stage 2
stage2_dry = 4000.0        # kg
stage2_fuel = 107500.0     # kg
stage2_thrust = 934000.0   # N
stage2_burn_time = 397     # seconds

# Constants
g = 9.8      # m/s^2
dt = 0.1     # time step in seconds
max_time = 1000  # safety limit in seconds

# Initial conditions
y = 0.0
v = 0.0
t = 0.0

# Stage control
current_stage = 1
fuel_mass = stage1_fuel
dry_mass = stage1_dry
thrust = stage1_thrust
burn_time = stage1_burn_time
time_in_stage = 0.0

# Data lists
time = []
height = []
velocity = []
acceleration = []

print("Starting Falcon 9 Simulation...\n")

# ------------------------
# Simulation loop
# ------------------------
while t <= max_time:
    # Burn fuel
    if fuel_mass > 0:
        burn_rate = fuel_mass / burn_time * dt
        fuel_mass -= burn_rate
        if fuel_mass < 0:
            fuel_mass = 0

    current_mass = dry_mass + fuel_mass
    thrust_now = thrust if fuel_mass > 0 else 0
    weight = current_mass * g
    net_force = thrust_now - weight

    # Physics
    a = net_force / current_mass
    v += a * dt
    y += v * dt

    # Save data
    time.append(t)
    height.append(y)
    velocity.append(v)
    acceleration.append(a)

    # Print every 30 seconds in minutes
    if int(t) % 30 == 0:
        print(f"t={t/60:.1f} min, stage={current_stage}, mass={current_mass/1000:.1f}t, "
              f"thrust={thrust_now/1000:.1f}kN, v={v:.2f}m/s, y={y/1000:.2f}km")

    # Stage separation
    if current_stage == 1 and time_in_stage >= stage1_burn_time:
        current_stage = 2
        fuel_mass = stage2_fuel
        dry_mass = stage2_dry
        thrust = stage2_thrust
        burn_time = stage2_burn_time
        time_in_stage = 0.0
        print(f"Stage 1 separation at t={t/60:.1f} min, y={y/1000:.2f} km")

    # Stop when rocket hits ground after coasting
    if y <= 0 and v <= 0 and t > 0:
        y = 0
        break

    # Update time
    t += dt
    time_in_stage += dt

# ------------------------
# Results
max_height = max(height)
max_velocity = max(velocity)
print(f"\nFalcon 9 Simulation Complete")
print(f"Max height: {max_height:.2f} m ({max_height/1000:.2f} km)")
print(f"Max velocity: {max_velocity:.2f} m/s")
print(f"Total flight time: {t/60:.1f} min")

# ------------------------
# Convert time to minutes for plotting
time_min = [ti/60 for ti in time]

# ------------------------
# Plot altitude, velocity, acceleration vs time (in minutes)
plt.figure(figsize=(12,10))

plt.subplot(3,1,1)
plt.plot(time_min, [h/1000 for h in height], 'b', linewidth=2)
plt.ylabel("Altitude (km)")
plt.grid(True)

plt.subplot(3,1,2)
plt.plot(time_min, velocity, 'r', linewidth=2)
plt.ylabel("Velocity (m/s)")
plt.grid(True)

plt.subplot(3,1,3)
plt.plot(time_min, acceleration, 'g', linewidth=2)
plt.xlabel("Time (minutes)")
plt.ylabel("Acceleration (m/s²)")
plt.grid(True)

plt.suptitle("Falcon 9 Flight Simulation", fontsize=16)
plt.show()
