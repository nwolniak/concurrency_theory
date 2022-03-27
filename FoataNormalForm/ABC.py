class A:
    def __init__(self, i, k):
        self.i = i
        self.k = k

    def task(self, matrix):
        return matrix[self.k][self.i] / matrix[self.i][self.i]

    def __repr__(self):
        return "A_" + str(self.i) + "_" + str(self.k)

    def __eq__(self, other):
        if other.__class__ != self.__class__:
            return False
        if self.i == other.i and self.k == other.k:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.i, self.k))


class B:
    def __init__(self, i, j, k):
        self.i = i
        self.j = j
        self.k = k

    def task(self, matrix, multiplier):
        return matrix[self.i][self.j] * multiplier

    def __repr__(self):
        return "B_" + str(self.i) + "_" + str(self.j) + "_" + str(self.k)

    def __eq__(self, other):
        if other.__class__ != self.__class__:
            return False
        if self.i == other.i and self.j == other.j and self.k == other.k:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.i, self.j))


class C:
    def __init__(self, i, j, k):
        self.i = i
        self.j = j
        self.k = k

    def task(self, matrix, value_to_subtract):
        return matrix[self.k][self.j] - value_to_subtract

    def __repr__(self):
        return "C_" + str(self.i) + "_" + str(self.j) + "_" + str(self.k)

    def __eq__(self, other):
        if other.__class__ != self.__class__:
            return False
        if self.i == other.i and self.j == other.j and self.k == other.k:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.i, self.j))
