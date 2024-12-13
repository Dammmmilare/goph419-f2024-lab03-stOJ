#Test Case 2.
import time
import numpy as np 
import matplotlib.pyplot as plt
from src.ODE_Case_Solver import ode_freefall_euler, ode_freefall_rk4

def measure_simulation_time(solver, g0, dg_dz, cd_star, heights, dt_values):
    simulation_times = {H: [] for H in heights}

    for H in heights:
        for dt in dt_values:
            start_time = time.perf_counter()
            solver(g0, dg_dz, cd_star, H, dt)
            end_time = time.perf_counter()
            simulation_times[H].append(end_time - start_time)
    
    return simulation_times

# Parameter definition and coefficient calculation.
#Parameters:
phi = 51.0486 # Latitude in Calgary,Alberta.
g0 = 9.811636 # measured in  m/s^2.
dg_dz = 3.086*10-6 #g′ ≈ 0.3086 mGal/m where 1 Gal = 1 cm/s2, so in SI units, g′ ≈ (m/s2)/m.
rho_steel = 7800 # measured in  kg/m3.
d = 0.015 # density converted to m from cm (1.5cm).
μ_air =  1.827*10-5 # measured in kg/(m⋅s).

# Drag coefficient:
r = d / 2
volume = (4 / 3) * np.pi * r**3
mass = rho_steel *volume
cD = 6 * np.pi * μ_air * r
cd_star = cD / mass

# heights in meters
heights = [10, 20, 40]
dt_values = np.logspace(-4, -1, 10)

euler_times = measure_simulation_time(ode_freefall_euler, g0, dg_dz, cd_star, heights, dt_values )
rk4_times = measure_simulation_time(ode_freefall_rk4, g0, dg_dz, cd_star, heights, dt_values)

plt.figure(figsize=(12, 6))
for H in heights:
    plt.plot(dt_values, euler_times[H], label=f"Euler H={H}", marker='o', linestyle='--')
    plt.plot(dt_values, rk4_times[H], label=f"RK4 H={H}", marker='x', linestyle='-')

plt.xscale('log')
plt.yscale('log')
plt.xlabel("Time Step  Δt (s)")
plt.ylabel("Simulation time (s)")
plt.title("Simulatiofn Time vs. Time step for Euler and RK4 Methods")
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.show()