import numpy as np
import matplotlib.pyplot as plt

years = 40
remaining_fraction = 0.85
mass = np.zeros(years + 1)
mass[0] = 20.0

for n in range(years):
    if n < 10:
        input_mass = 8.0
    else:
        input_mass = 2.0

    mass[n + 1] = remaining_fraction * mass[n] + input_mass

time = np.arange(years + 1)

plt.plot(time, mass, "o-")
plt.xlabel("Time (years)")
plt.ylabel("Pollutant mass (kg)")
plt.show()

# Try:
# 1. Change the year of the intervention.
# 2. Change remaining_fraction.
# 3. Find the long-term level for constant input.
