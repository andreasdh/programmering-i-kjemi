def f(x):
    return x**3

def left_rectangle(f, a, b, n):
    h = (b - a) / n
    area = 0.0

    for k in range(n):
        # Complete the x value and the area update.
        x = a
        area = area

    return area

def midpoint_rectangle(f, a, b, n):
    h = (b - a) / n
    area = 0.0

    for k in range(n):
        # Complete the midpoint x value and the area update.
        x = a
        area = area

    return area

for n in [10, 100, 1000]:
    print("n =", n)
    print("Left:", left_rectangle(f, 0, 5, n))
    print("Midpoint:", midpoint_rectangle(f, 0, 5, n))
