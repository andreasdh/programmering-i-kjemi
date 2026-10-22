import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return np.sin(x)

def forward(f, x, h):
    return (f(x + h) - f(x)) / h

def backward(f, x, h):
    # Complete this line.
    return 0

def central(f, x, h):
    # Complete this line.
    return 0

x = 1.0
exact = np.cos(x)
h_values = np.logspace(-1, -12, 12)

forward_error = []
central_error = []

for h in h_values:
    forward_error.append(abs(forward(f, x, h) - exact))
    central_error.append(abs(central(f, x, h) - exact))

plt.loglog(h_values, forward_error, "o-", label="Forward")
plt.loglog(h_values, central_error, "o-", label="Central")
plt.xlabel("h")
plt.ylabel("Absolute error")
plt.legend()
plt.show()
