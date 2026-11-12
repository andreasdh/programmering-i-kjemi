import math

C = 0.010
Ka = 1.75e-5
Kw = 1.0e-14

def charge_balance(h):
    A_minus = C * Ka / (h + Ka)
    OH = Kw / h
    return h - A_minus - OH

def bisection(f, a, b, tol=1e-10, max_iter=100):
    # Complete the algorithm below.
    for i in range(max_iter):
        m = (a + b) / 2

        # 1. Stop if abs(f(m)) is smaller than tol.
        # 2. Keep the half-interval that contains a sign change.

    return m

# Try the interval below when your function is complete.
# h = bisection(charge_balance, 1e-7, 1e-2)
# pH = -math.log10(h)
# print("pH =", pH)
