import numpy as np
import matplotlib.pyplot as plt

k = 0.030
A0 = 1.00
dt = 1.0
t_end = 150.0

time = np.arange(0, t_end + dt, dt)
A = np.zeros(len(time))
A[0] = A0

for i in range(len(time) - 1):
    dA_dt = -k*A[i]
    A[i + 1] = A[i] + dA_dt*dt

A_exact = A0*np.exp(-k*time)

plt.plot(time, A, label="Forward Euler")
plt.plot(time, A_exact, "--", label="Analytical")
plt.xlabel("Time (s)")
plt.ylabel("[A] (mol/L)")
plt.legend()
plt.show()
