def make_frequency(fileIn):
    d = dict()
    for line in fileIn:
        for c in line:
            if c not in d:
                d[c] = 1
            else:
                d[c] += 1
    return d

fileIn = open("text1.txt", "r")
hist = make_frequency(fileIn)
print(hist)
print(sorted(hist.items(), key=
    lambda kv: (kv[1], kv[0])))
