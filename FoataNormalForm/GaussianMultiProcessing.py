from ABC import A, B, C
from concurrent.futures import ProcessPoolExecutor
from time import time
import numpy as np


class GaussianElimination:
    def __init__(self, matrix, n, fnf):
        self.matrix = matrix
        self.n = n
        self.fnf = fnf
        self.multipliers = dict()
        self.values_to_subtract = dict()

    def tasks(self, task_name):
        if isinstance(task_name, A):
            return task_name.task(self.matrix)
        elif isinstance(task_name, B):
            i, k = task_name.i, task_name.k
            return task_name.task(self.matrix, self.multipliers.get((k, i)))
        elif isinstance(task_name, C):
            i, j, k = task_name.i, task_name.j, task_name.k
            return task_name.task(self.matrix, self.values_to_subtract.get((k, j, i)))

    def compute(self, filename=None):
        start1 = time()
        for idx_i, _fnf in enumerate(self.fnf):
            with ProcessPoolExecutor() as executor:
                start2 = time()
                results = executor.map(self.tasks, _fnf)
                for idx_j, result in enumerate(results):
                    if isinstance(_fnf[idx_j], A):
                        i, k = _fnf[idx_j].i, _fnf[idx_j].k
                        self.multipliers[(k, i)] = result
                    elif isinstance(_fnf[idx_j], B):
                        i, j, k = _fnf[idx_j].i, _fnf[idx_j].j, _fnf[idx_j].k
                        self.values_to_subtract[(k, j, i)] = result
                    elif isinstance(_fnf[idx_j], C):
                        j, k = _fnf[idx_j].j, _fnf[idx_j].k
                        self.matrix[k, j] = result
            print("{} executed {:.4f}s : {}".format(idx_i, time() - start2, _fnf))
        print("executed in {:.4f}s".format(time() - start1))

        self._back_substitution()
        self._save(filename)

    def _back_substitution(self):
        for i in range(self.n - 1, -1, -1):
            tmp = np.dot(self.matrix[i, i+1:self.n], self.matrix[i+1:self.n, self.n])
            self.matrix[i, self.n] = (self.matrix[i, self.n] - tmp) / self.matrix[i, i]
            self.matrix[i, i+1:self.n] *= 0
            self.matrix[i, i] /= self.matrix[i, i]

    def _save(self, filename=None):
        if filename:
            with open(filename, "w+") as f:
                f.write("{}\n".format(self.n))
                for row in self.matrix:
                    for val in row[:-1]:
                        f.write("{} ".format(val))
                    f.write("\n")
                for i in range(self.n):
                    f.write("{} ".format(self.matrix[i, self.n]))

                f.close()
