from alphabet import alphabet
from DependencySet import compute_D
from DiekertGraph import DiekertGraph
from GaussianMultiProcessing import GaussianElimination
import numpy as np
from ABC import A, B, C
import sys


def read_values(file_name):
    with open(file_name, "r") as file:
        text = file.readlines()
        for i, line in enumerate(text):
            if i == 0:
                n = int(line)
                matrix = np.zeros((n, n+1))
            elif i <= n:
                for j, elem in enumerate(list(map(float, line.split(" ")[:-1]))):
                    matrix[i-1, j] = elem
            else:
                for j, elem in enumerate(list(map(float, line.split(" ")[:-1]))):
                    matrix[j, n] = elem
    return n, matrix


def generate_fnf(n):
    fnf = []
    for i in range(n-1):
        fnf.append([])
        fnf.append([])
        fnf.append([])
        for k in range(i+1, n):
            fnf[i*3].append(A(i, k))
        for k in range(i+1, n):
            for j in range(i, n + 1):
                fnf[i*3+1].append(B(i, j, k))
        for k in range(i+1, n):
            for j in range(i, n + 1):
                fnf[i*3+2].append(C(i, j, k))
    return fnf


def main(input_file="input.txt", output_file="output.txt", graph=False):
    n, matrix = read_values(input_file)
    FNF = []
    if graph:
        W = alphabet(n)
        print("W : ", W)
        D = compute_D(n)
        print(D)

        G = DiekertGraph(W, D, n)
        FNF = G.get_FNF()
        G.save("graph.dot", "graph.png")
    else:
        FNF = generate_fnf(n)

    scheduler = GaussianElimination(matrix, n, FNF)
    scheduler.compute(output_file)


if __name__ == '__main__':
    if len(sys.argv) - 1 == 2:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) - 1 == 3:
        main(sys.argv[1], sys.argv[2], bool(int(sys.argv[3])))
    else:
        main()