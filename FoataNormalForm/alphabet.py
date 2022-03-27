from ABC import A, B, C

def alphabet(n):
    w = []
    for i in range(n-1):
        for k in range(i+1, n):
            w.append(A(i, k))
            for j in range(i, n + 1):
                w.append(B(i, j, k))
                w.append(C(i, j, k))
    return w