from functools import reduce

from .utils import is_prime



class GF:
    def __init__(self, pow: int, val: int):
        if not isinstance(pow, int):
            raise TypeError("Power must be int")
        if not isinstance(val, int):
            raise TypeError("Value must be int")
        if pow < 2:
            raise ValueError('Invalid GF power')
        if not is_prime(pow):
            raise ValueError('GF must have prime order')
        if val < 0 or val > pow - 1:
            raise ValueError('Invalid GF elem value')
        self.pow = pow
        self.val = val

    def ord(self) -> int:
        i = 1
        val = self.val
        while val != 1:
            val = (val * self.val) % self.pow
            i += 1

        return i

    def is_same_field(self, other: "GF") -> bool:
        return isinstance(other, GF) and self.pow == other.pow

    def __str__(self) -> str:
        return str(self.val)

    def __neg__(self) -> "GF":
        return GF(self.pow, (self.pow - self.val) % self.pow)

    def __add__(self, other: "GF") -> "GF":
        if not self.is_same_field(other):
            raise ValueError('Invalid fields in elems add')
        
        return GF(self.pow, (self.val + other.val) % self.pow)

    def __sub__(self, other: "GF") -> "GF":
        if not self.is_same_field(other):
            raise ValueError('Invalid fields in elems sub')
        
        return self + -other

    def __invert__(self) -> "GF":
        r1, r2 = self.val, self.pow
        x1, x2 = 1, 0

        while r2 != 0:
            q = r1 // r2
            r2, r1 = r1 - r2 * q, r2
            x2, x1 = x1 - x2 * q, x2

        return GF(self.pow, (self.pow + x1) % self.pow)

    def __mul__(self, other: "GF") -> "GF":
        if not self.is_same_field(other):
            raise ValueError('Invalid fields in elems mul')
        
        return GF(self.pow, (self.val * other.val) % self.pow)

    def __truediv__(self, other: "GF") -> "GF":
        if not self.is_same_field(other):
            raise ValueError('Invalid fields in elems div')
        
        return self * ~other

    def __pow__(self, power, modulo=None) -> "GF":
        if power == 0:
            return GF(self.pow, 1)
        
        return reduce(lambda a, b: a * b, [self for i in range(power)])

    def __gt__(self, other: "GF") -> bool:
        if self.is_same_field(other):
            return self.val > other.val
        
        return self.val > other

    def __lt__(self, other: "GF") -> bool:
        if self.is_same_field(other):
            return self.val < other.val
        
        return self.val < other

    def __ge__(self, other: "GF") -> bool:
        return self > other or self == other

    def __eq__(self, other: "GF") -> bool:
        if self.is_same_field(other):
            return self.val == other.val
        return self.val == other

    def __ne__(self, other: "GF") -> bool:
        return not self == other

    def __abs__(self) -> "GF":
        return self

    def __int__(self) -> int:
        return int(self.val)