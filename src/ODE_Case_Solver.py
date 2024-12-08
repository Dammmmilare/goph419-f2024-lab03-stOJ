import numpy as np

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


def ode_freefall_euler(g0, dg_dz, cd_star, H, dt):
    t, z, v = [0], [0], [0]
    while z[-1] < H:
        g = g0 - dg_dz * z[-1]
        drag = cd_star * v[-1]
        a = g - drag
        v_new = v[-1] + a * dt
        z_new = z[-1] + v[-1] * dt
        t_new = t[-1] + dt
        if z_new > H:
            dt_last = (H -z[-1]) / v[-1]
            z_new = H
            t_new = t[-1] + dt_last
            v_new = v[-1] + a * dt_last
        t.append(t_new)
        z.append(z_new)
        v.append(v_new)
    return np.array(t), np.array(z), np.array(v)

def ode_freefall_rk4(go, dg_dz, cd_star, H, dt):
    t, z, v = [0], [0], [0]
    while z[-1] < H:
        g = g0 - dg_dz * z[-1]
        drag = cd_star * v[-1]

        def acceleration(z, v):
            return g - cd_star * v #* z
        
        def dz_dt(v):
            return v

        k1_v = acceleration(z[-1], v[-1]) * dt
        k1_z = dz_dt(v[-1]) * dt

        k2_v = acceleration(z[-1] + k1_z / 2, v[-1] + k1_v / 2) * dt
        k2_z = dz_dt(v[-1] + k1_v / 2) * dt

        k3_v = acceleration(z[-1] + k2_z / 2, v[-1] + k2_v / 2) * dt
        k3_z = dz_dt(v[-1] + k2_v / 2) * dt

        k4_v = acceleration(z[-1] + k3_z / 2, v[-1] + k3_v / 2) * dt
        k4_z = dz_dt(v[-1] + k3_v) * dt

        dv = (k1_v + 2 * k2_v + 2 * k3_v + k4_v) / 6
        dz = (k1_z + 2 * k2_z + 2 * k3_z + k4_z) / 6

        v_new = v[-1] + dv
        z_new = z[-1] + dv
        t_new = t[-1] + dv

        if z_new > H: 
            dt_last = (H -z[-1]) / v[-1]
            z_new = H
            t_new = t[-1] + dt_last
            v_new = v[-1] + acceleration(z[-1], v[-1]) * dt_last
        t.append(t_new)
        z.append(z_new)
        v.append(v_new)
    return np.array(t), np.array(z), np.array(v)

import time
import numpy as np 
import matplotlib.pyplot as plt

def measure_simulation_time(solver, g0, dg_dz, cd_star, heights, dt_values):
    simulation_times = {H: [] for H in heights}

    for H in heights:
        for dt in dt_values:
            start_time = time.perf_counter()
            solver(g0, dg_dz, cd_star, H, dt)
            end_time = time.perf_counter()
            simulation_times[H].append(end_time - start_time)
    
    return simulation_times

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
plt.ylabel("Simulatiofn Time vs. Time step for Euler and RK4 Methods")
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.show()

