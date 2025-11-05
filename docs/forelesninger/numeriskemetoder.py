def newtons(f, fder, x0, nmaks = 100, tol = 1E-12):
    """
    Newton's method for finding a root of f.
    
    f: function for which we want to find a root
    fder: derivative of f
    x0: initial guess
    nmaks: maximum number of iterations
    tol: tolerance for convergence
    Returns an approximation to a root of f.
    """
    x = x0
    i = 0
    while abs(f(x)) > tol and i < nmaks:
        x = x - f(x)/fder(x)
        i = i + 1
    return x

def rektangelmetoden_venstre(f, a, b, n = 100000):
    dx = (b - a)/n # Bredden av hvert rektangel
    A = 0 # Arealet av rektanglene
    x = a
    for i in range(n):
        # Summere opp arealet av hvert rektangel
        A = A + f(x) * dx
        x = x + dx
    return A

def rektangelmetoden_høyre(f, a, b, n = 100000):
    dx = (b - a)/n # Bredden av hvert rektangel
    A = 0 # Arealet av rektanglene
    x = a + dx
    for i in range(n):
        # Summere opp arealet av hvert rektangel
        A = A + f(x) * dx
        x = x + dx
    return A

def rektangelmetoden_midtpunkt(f, a, b, n = 100000):
    dx = (b - a)/n # Bredden av hvert rektangel
    A = 0 # Arealet av rektanglene
    x = a + dx/2
    for i in range(n):
        # Summere opp arealet av hvert rektangel
        A = A + f(x) * dx
        x = x + dx
    return A

def trapesmetoden(f, a, b, n = 100000):
    dx = (b - a)/n # Bredden av hvert rektangel
    A = (f(a) + f(b))/2*dx # Arealet av rektanglene
    x = a
    for i in range(1, n):
        # Summere opp arealet av hvert rektangel
        A = A + f(x) * dx
        x = x + dx
    return A