import random
import copy

class Matrix:
    def __init__(self, n, m, mtrx=None):
        if n < 1:
            raise ValueError("Invalid rows value")
        if m < 1:
            raise ValueError("Invalid columns value")

        if mtrx is None:
            mtrx = [[0 for i in range(m)] for j in range(n)]
        elif len(mtrx) != n or len(mtrx[0]) != m:
            raise ValueError("Invalid mtrx in init")

        self.n = n
        self.m = m
        self.mtrx = mtrx

    def __str__(self):
        s = ''
        for i in range(self.n):
            for j in range(self.m):
                s += str(self.mtrx[i][j]).rjust(3, ' ')
            s += '\n'
        return s

    def __neg__(self):
        return Matrix(self.n, self.m, [[-i for i in self.mtrx[j]] for j in range(self.m)])

    def __add__(self, other):
        if self.n != other.n or self.m != other.m:
            raise ValueError('Can\'t add mtrxs')

        return Matrix(self.n, self.m, [[a + b for a, b in zip(self.mtrx[i], other.mtrx[i])] for i in range(self.n)])

    def __sub__(self, other):
        return self + -other

    def __mul__(self, other):
        if self.m != other.n:
            raise ValueError('Can\'t mult mtrxs')

        res_mtrx = Matrix(self.n, other.m)
        for i in range(res_mtrx.n):
            for j in range(res_mtrx.m):
                res_mtrx.mtrx[i][j] = sum([self.mtrx[i][k] * other.mtrx[k][j] for k in range(self.m)],
                                          self.mtrx[0][0] - self.mtrx[0][0])

        return res_mtrx

    def __eq__(self, other):
        if self.n is not other.n or self.m is not other.m:
            return False
        for i in range(self.n):
            for j in range(self.m):
                if self.mtrx[i][j] is not other.mtrx[i][j]:
                    return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def set_rand(self, min_val, max_val):
        for i in range(0, self.n):
            for j in range(0, self.m):
                self.mtrx[i][j] = random.randint(min_val, max_val)

    def set_mtrx(self, mtrx_val):
        if len(mtrx_val) != self.n or len(mtrx_val[0]) != self.m:
            raise ValueError("Invalid mtrx in set_mtrx() method")
        self.mtrx = copy.deepcopy(mtrx_val)

    def get_transposed(self):
        return Matrix(self.m, self.n, [[self.mtrx[j][i] for j in range(self.n)] for i in range(self.m)])
