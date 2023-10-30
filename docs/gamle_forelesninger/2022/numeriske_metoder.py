def framoverdifferanse(f, a, dx = 1E-8):
    """
    Deriverer en funksjon f i punktet a.
    ----------
    f : function
        Funksjonen vi skal derivere.
    a : float
        Punktet vi skal evaluere den deriverte i.
    dx : float, optional
        Endringen i x-verdier. The default is 1E-8.

    Returns
    -------
    der : float.
          Den deriverte av f(a)
    """
    der = (f(x + dx) - f(x))/dx
    return der
