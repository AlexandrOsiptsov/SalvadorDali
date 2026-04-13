import random
import copy
from .Polynom import Polynom
from .GF import GF

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
        return s[:-1]

    def __neg__(self):
        return Matrix(self.n, self.m, [[-i for i in self.mtrx[j]] for j in range(self.m)])

    def __add__(self, other: 'Matrix'):
        if self.n != other.n or self.m != other.m:
            raise ValueError('Can\'t add mtrxs')

        return Matrix(self.n, self.m, [[a + b for a, b in zip(self.mtrx[i], other.mtrx[i])] for i in range(self.n)])

    def __sub__(self, other: 'Matrix'):
        return self + -other

    def __mul__(self, other: 'Matrix'):
        if self.m != other.n:
            raise ValueError('Can\'t mult mtrxs')

        res_mtrx = Matrix(self.n, other.m)
        for i in range(res_mtrx.n):
            for j in range(res_mtrx.m):
                res_mtrx.mtrx[i][j] = sum([self.mtrx[i][k] * other.mtrx[k][j] for k in range(self.m)],
                                          self.mtrx[0][0] - self.mtrx[0][0])
        return res_mtrx

    @classmethod
    def identity(cls, n, zero, one):
        return cls(
            n, n,
            [
                [one if i == j else zero for j in range(n)]
                for i in range(n)
            ]
        )

    def __rmul__(self, other):
        return Matrix(self.n, self.m, [[other * self.mtrx[i][j] for j in range(self.m)] for i in range(self.n)])

    def __pow__(self, power):
        if not isinstance(power, int):
            raise ValueError("The exponent must be an integer")
        if self.n != self.m:
            raise ValueError("Only square matrices can be raised to a power")
        if power < 0:
            raise ValueError("Negative exponents are not supported")

        # Identity matrix
        zero = self.mtrx[0][0] - self.mtrx[0][0]
        result = Matrix.identity(self.n, zero, zero + 1)

        temp = copy.deepcopy(self)
        exp = power
        while exp > 0:
            if exp % 2 == 1:
                result = result * temp
            temp = temp * temp
            exp //= 2
        return result

    def __eq__(self, other: 'Matrix'):
        if self.n is not other.n or self.m is not other.m:
            return False
        for i in range(self.n):
            for j in range(self.m):
                if self.mtrx[i][j] != other.mtrx[i][j]:
                    return False
        return True

    def __ne__(self, other: 'Matrix'):
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

    def determinant(self):
        if self.n != self.m:
            raise ValueError("Determinant is only defined for square matrices.")

        # Base case for 1x1 matrix
        if self.n == 1:
            return self.mtrx[0][0]

        # Base case for 2x2 matrix
        if self.n == 2:
            return self.mtrx[0][0] * self.mtrx[1][1] - self.mtrx[0][1] * self.mtrx[1][0]

        det = self.mtrx[0][0] - self.mtrx[0][0]  # get "zero" like object for type
        for c in range(self.n):
            # Build the minor matrix
            minor = []
            for i in range(1, self.n):
                row = []
                for j in range(self.n):
                    if j != c:
                        row.append(self.mtrx[i][j])
                minor.append(row)
            # sign is + if c even, - if c odd
            sign = (-1) ** c
            det += sign * self.mtrx[0][c] * Matrix(self.n - 1, self.n - 1, minor).determinant()
        return det


    def char_eq(self) -> Polynom:
        zero = self.mtrx[0][0] - self.mtrx[0][0]
        one = zero + 1
        return (self - Matrix.identity(self.n, zero, one).__rmul__(Polynom([zero, one], zero, one))).determinant()
