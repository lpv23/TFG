def potencias2(n):
    if n == 1:
        return 2
    return potencias2(n-1) + potencias2(n-1)
