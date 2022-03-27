from ABC import A, B, C

class DependencySet:
    def __init__(self):
        self.items = []

    def append(self, s, t):
        self.items.append((s, t))

    def __str__(self, n=5):
        _str = ""
        _str += "D = sym{{"
        for idx, item in enumerate(self.items):
            _str += "(" + str(item[0]) + ", " + str(item[1]) + "), "
            if (idx + 1) % n == 0:
                _str += "\n"
        _str += "}+} U I_sigma"

        return _str

    def __contains__(self, item):
        for s_item in self.items:
            if s_item[0] == item[0] and s_item[1] == item[1]:
                return True
        return False


def compute_D(n):
    D = DependencySet()
    for i in range(n):
        for k in range(i + 1, n):
            for j in range(i, n + 1):
                D.append(A(i, k), B(i, j, k))
                D.append(B(i, j, k), C(i, j, k))

    for i in range(n - 1):
        for k in range(i + 2, n):
            D.append(C(i, i + 1, k), A(i + 1, k))
            D.append(C(i, i + 1, i + 1), A(i + 1, k))

    for i in range(n - 1):
        for j in range(i + 2, n + 1):
            for k in range(i + 2, n):
                D.append(C(i, j, i + 1), B(i + 1, j, k))
                D.append(C(i, j, k), C(i + 1, j, k))
    return D