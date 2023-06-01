def potencias2(n):
    if n == 0:
        return 1
    return potencias2(n-1) + potencias2(n-1)
