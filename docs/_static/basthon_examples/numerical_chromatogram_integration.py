import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

time = np.array([4.0, 4.2, 4.4, 4.6, 4.8, 5.0, 5.2, 5.4, 5.6, 5.8, 6.0])
signal = np.array([0.01, 0.04, 0.16, 0.50, 0.88, 1.00, 0.82, 0.46, 0.17, 0.05, 0.01])

area = integrate.trapezoid(signal, x=time)

plt.plot(time, signal, "o-")
plt.fill_between(time, signal, alpha=0.25)
plt.xlabel("Retention time (min)")
plt.ylabel("Detector signal")
plt.show()

print("Peak area =", area, "signal·min")
