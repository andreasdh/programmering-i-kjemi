import numpy as np
import matplotlib.pyplot as plt

volume = np.array([20.0, 22.0, 23.0, 24.0, 24.5, 25.0, 25.5, 26.0, 27.0, 28.0, 30.0])
pH = np.array([2.90, 3.20, 3.45, 3.85, 4.35, 7.00, 9.65, 10.15, 10.55, 10.80, 11.10])

dpH_dV = np.diff(pH) / np.diff(volume)
volume_mid = (volume[:-1] + volume[1:]) / 2

equivalence_volume = volume_mid[np.argmax(dpH_dV)]

plt.plot(volume_mid, dpH_dV, "o-")
plt.axvline(equivalence_volume, linestyle="--")
plt.xlabel("Added NaOH (mL)")
plt.ylabel("Delta pH / Delta V")
plt.show()

print("Estimated equivalence volume:", equivalence_volume, "mL")
