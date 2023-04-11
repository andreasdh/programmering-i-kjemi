def eulers_metode(yder, y0, x0, x_slutt, dx=1E-5):
    x_liste = [x0]
    y_liste = [y0]
    x = x0
    y = y0
    while x <= x_slutt:
        y = y + yder(x,y)*dx
        x = x + dx
        y_liste.append(y)
        x_liste.append(x)
    return x_liste, y_liste