import copy
import math
from functools import reduce
from typing import Tuple, List

from .GF import GF
from .Vector import Vector



class Polynom:
    def __init__(self, init_vect, zero_elem, id_elem):
        if len(init_vect) < 1:
            raise ValueError('Invalid vector dimension')
        if type(init_vect[0]) != type(zero_elem) or type(zero_elem) != type(id_elem):
            raise ValueError('Invalid elements types')
        if zero_elem == id_elem:
            raise ValueError('Zero elem can\'t be equal to id elem in field')

        self.lst = init_vect
        self.zero = zero_elem
        self.id = id_elem


    def is_same_field(self, other) -> bool:
        if not isinstance(other, Polynom):
            raise TypeError("Invalid type in field comparison")

        if not isinstance(self.lst[0], other.lst[0]):
            return False
        
        if self.zero != other.zero or self.id != other.id:
            return False
        
        return True


    def __str__(self) -> str:
        if self.is_null():
            return '0'
        res = ''
        sign_flag = False
        for i in range(len(self) - 1, -1, -1):
            if self.lst[i] == self.zero:
                continue

            if self.lst[i] > 0 and sign_flag:
                res += '+ '
            elif self.lst[i] < 0:
                res += '- '

            sign_flag = True

            if abs(self.lst[i]) != self.id or i == 0:
                if isinstance(self.lst[i], float) and math.modf(self.lst[i])[0] == 0:
                    res += str(int(abs(self.lst[i])))
                else:
                    res += str(abs(self.lst[i]))

            if i > 1:
                res += str(f'x^{str(i)} ')
            elif i == 1:
                res += 'x '

        if res[-1] == ' ':
            res = res[:-1]
        return res


    def __neg__(self) -> "Polynom":
        return Polynom([-i for i in self.lst], self.zero, self.id)


    def __add__(self, other: "Polynom") -> "Polynom":
        if not self.is_same_field(other):
            raise ValueError('Invalid polynomials add')

        zero_arr = [self.zero for i in range(abs(len(self.lst) - len(other.lst)))]

        if len(self.lst) > len(other.lst):
            zip_arr = zip(self.lst, other.lst + zero_arr)
        else:
            zip_arr = zip(self.lst + zero_arr, other.lst)

        return Polynom([a + b for a, b in zip_arr], self.zero, self.id)


    def __sub__(self, other: "Polynom") -> "Polynom":
        if not self.is_same_field(other):
            raise ValueError('Invalid polynomials sub')
        
        return self + -other


    def __mul__(self, other: "Polynom") -> "Polynom":
        if isinstance(other, Polynom):
            return sum([(self * i).inc_dim(ind) for ind, i in enumerate(other.lst)],
                       Polynom([self.zero], self.zero, self.id))
        else:
            return Polynom([i * other for i in self.lst], self.zero, self.id)


    def __truediv__(self, other: "Polynom") -> Tuple["Polynom", "Polynom"]:
        if not isinstance(other, Polynom):
            raise TypeError('Invalid type in polynom division')
        
        if self.zero != other.zero or self.id != other.id:
            raise ValueError('Invalid polynoms divide')
        
        if self.deg() < other.deg():
            return Polynom([self.zero], self.zero, self.id), self
        
        if other.is_null():
            raise ValueError('Null polynom divide')

        self = self.compact()
        other = other.compact()

        res_plnm = Polynom([self.zero for i in range(len(self))], self.zero, self.id)
        divisible_plnm: Polynom = self

        while True:
            # Difference in degree
            deg_diff = divisible_plnm.deg() - other.deg()
            # Difference in senior coefficient
            coef_diff = divisible_plnm.lst[-1] / other.lst[-1]

            divisible_plnm = (divisible_plnm - Polynom([coef_diff * i for i in other.inc_dim(deg_diff).lst], self.zero,
                                                    self.id)).compact()
            res_plnm.lst[deg_diff] = coef_diff
            if divisible_plnm.deg() >= other.deg() and not divisible_plnm.is_null():
                deg1 = divisible_plnm.deg()
                deg2 = other.deg()
                continue
            break

        return res_plnm, divisible_plnm


    def __mod__(self, other: "Polynom") -> "Polynom":
        if not isinstance(other, Polynom):
            raise TypeError('Invalid type in polynom mod')
        
        return (self / other)[1]


    def __pow__(self, power, modulo=None):
        if power == 0:
            return Polynom([self.id], self.zero, self.id)
        return reduce(lambda a, b: a * b, [self for i in range(power)])


    def __len__(self) -> int:
        return len(self.lst)


    def __key(self):
        return ''.join(str(i) for i in self.compact().lst) + str(self.zero) + str(self.id)


    def __eq__(self, other: "Polynom") -> bool:
        if isinstance(other, Polynom):
            return self.__key() == other.__key()
        return NotImplemented


    def __hash__(self):
        return hash(self.__key())


    def deg(self) -> int:
        for i in range(len(self.lst) - 1, 0, -1):
            if self.lst[i] != self.zero:
                return i
        return 0


    def compact(self) -> "Polynom":
        return Polynom([self.lst[i] for i in range(self.deg() + 1)], self.zero, self.id)


    def inc_dim(self, k=1) -> "Polynom":
        return Polynom([self.zero for i in range(k)] + self.lst, self.zero, self.id)


    def is_null(self) -> bool:
        for i in self.lst:
            if i != self.zero:
                return False
        return True


    def func(self, x):
        res = (x ** 0) * self.lst[0]
        for i in range(1, len(self.lst)):
            res += (x ** i) * self.lst[i]

        return res


    def factor_ring(self) -> List["Polynom"]:
        if not isinstance(self.id, GF):
            raise ValueError('Factor ring with coefs in infinity field is infinity')

        factor_ring = []
        vect = Vector([self.zero for i in range(self.deg())], self.zero, self.id)

        factor_ring.append(Polynom(vect.lst, self.zero, self.id))
        while vect.increment():
            factor_ring.append(copy.deepcopy(Polynom(vect.lst, self.zero, self.id)))

        return factor_ring


    def is_primitive(self) -> bool:
        if not isinstance(self.id, GF):
            return NotImplemented

        for plnm in self.factor_ring():
            if (self.func(plnm) % self).is_null():
                plnm_degs = set()
                for i in range(1, self.id.pow ** self.deg()):
                    plnm_degs.add(plnm ** i % self)
                if len(plnm_degs) == self.id.pow ** self.deg() - 1:
                    return True

        return False
    



def euclid_polynom(p1: Polynom, p2: Polynom) -> Polynom:
    while (not p1.is_null()) and (not p2.is_null()):
        if p1.deg() > p2.deg():
            p1 = (p1 / p2)[1]
        else:
            p2 = (p2 / p1)[1]

    if p1.is_null():
        return p2
    else:
        return p1