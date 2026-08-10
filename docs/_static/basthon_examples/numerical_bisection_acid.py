import numpy as np

Ka = 1.75e-5
Kw = 1.0e-14
c0 = 0.010

def charge_balance(h):
    return h - Ka*c0/(h + Ka) - Kw/h

def bisection(f, a, b, tolerance=1e-10, max_iterations=100):
    if f(a) * f(b) > 0:
        raise ValueError("f(a) and f(b) must have opposite signs.")

    for _ in range(max_iterations):
        c = (a + b) / 2
        if abs(f(c)) < tolerance:
            return c
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c

    raise RuntimeError("The method did not converge.")

h = bisection(charge_balance, 1e-5, 1e-1)
print("pH =", -np.log10(h))
