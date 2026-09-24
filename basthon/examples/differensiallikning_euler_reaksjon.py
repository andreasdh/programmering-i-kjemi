import numpy as np
import matplotlib.pyplot as plt

k = 0.15
A0 = 1.0
dt = 0.5
t_end = 30

t = np.arange(0, t_end + dt, dt)
A = np.zeros(len(t))
A[0] = A0

for n in range(len(t) - 1):
    rate = -k * A[n]
    A[n + 1] = A[n] + rate * dt

exact = A0 * np.exp(-k * t)

plt.plot(t, A, "o", label="Euler")
plt.plot(t, exact, label="Analytical")
plt.xlabel("Time")
plt.ylabel("[A]")
plt.legend()
plt.show()

# Try changing dt to 2.0, 1.0, 0.1 and 0.01.
