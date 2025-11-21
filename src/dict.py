def freq_chaine(chaine):
    d = dict()
    for c in chaine:
        if c in d:
            d[c] += 1
        else:
            d[c] = 1

    return d

print(freq_chaine("abbabba!"))
