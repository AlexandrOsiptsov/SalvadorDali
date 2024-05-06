import copy
from typing import List, TypeVar, Generic

from .GF import GF
from .utils import base_str


T = TypeVar('T')  # Обобщенный тип


class Vector(Generic[T]):
    def __init__(self, init_vect: List[T], zero_elem: T, id_elem: T):
        if len(init_vect) < 1:
            raise ValueError('Invalid vector dimension')
        
        if zero_elem == id_elem:
            raise ValueError('Zero elem can\'t be equal to id elem in field')

        self.lst = init_vect
        self.zero = zero_elem
        self.id = id_elem


    def is_same_ring(self, other: "Vector") -> bool:
        if not isinstance(other, Vector):
            raise TypeError("Invalid vectors fields comparison")
        
        if type(self.lst[0]) != type(other.lst[0]):
            return False
        
        if self.zero != other.zero or self.id != other.id:
            return False
        
        if len(self.lst) != len(other.lst):
            return False
        
        return True


    def __str__(self) -> str:
        return ''.join([str(i) + ' ' for i in self.lst])

    def is_null(self) -> bool:
        for i in self.lst:
            if i != self.zero:
                return False
        return True

    def increment(self) -> "Vector":
        res_vect = copy.deepcopy(self)
        for i in range(len(res_vect.lst)):
            rem, res_vect.lst[i] = res_vect.lst[i], res_vect.lst[i] + res_vect.id
            if rem > res_vect.lst[i]:
                continue
            break

        if res_vect.is_null():
            return None
        return res_vect
    

    def reversed(self) -> "Vector[T]":
        return Vector(self.lst[::-1], self.zero, self.id)
    

    @staticmethod
    def from_int(val: int, base: int, size: int = None) -> "Vector[GF]":
        num_string = base_str(val, base)

        if size is not None:
            num_string = num_string.zfill(size)

        return Vector([GF(base, int(elem)) for elem in num_string], GF(base, 0), GF(base, 1))
    

    def gf_ind(self: "Vector[GF]") -> int:
        if not isinstance(self.lst[0], GF):
            raise TypeError("Vector must contain GF objects")
        
        return sum([elem.val * pow(self.id.pow, ind) for ind, elem in enumerate(self.reversed().lst)])
    

    def gf_ring_add(self: "Vector[GF]", other: "Vector[GF]") -> "Vector[GF]":
        if not self.is_same_ring(other):
            raise TypeError("Vectors must be from the same ring")

        mod = pow(self.id.pow, len(self.lst))

        return Vector.from_int((self.gf_ind() + other.gf_ind()) % mod, self.id.pow, len(self.lst))


    def __getitem__(self, i) -> T:
        return self.lst[i]


    def __len__(self) -> int:
        return len(self.lst)


    def __neg__(self) -> "Vector[T]":
        return Vector([-i for i in self.lst], self.zero, self.id)


    def __add__(self, other: "Vector") -> "Vector":
        if not self.is_same_ring(other) or len(self) != len(other):
            raise ValueError('Invalid vector add')
        
        return Vector([a + b for a, b in zip(self.lst, other.lst)], self.zero, self.id)


    def __sub__(self, other: "Vector") -> "Vector":
        if not self.is_same_ring(other) or len(self) != len(other):
            raise ValueError('Invalid vector sub')
        return self + -other


    def __gt__(self,other: "Vector") -> "Vector":
        if not self.is_same_ring(other) or len(self) != len(other):
            raise ValueError('Invalid vector compare (>)')
        for i in range(len(self.lst) - 1, 0, -1):
            if self.lst[i] > other.lst[i]:
                return True
            elif self.lst[i] < other.lst[i]:
                return False
        return False


    def __eq__(self, other: "Vector") -> "Vector":
        if not self.is_same_ring(other) or len(self) != len(other):
            raise ValueError('Invalid vector compare (==)')
        for i in range(len(self.lst)):
            if self.lst[i] != other.lst[i]:
                return False
        return True


    def __ge__(self, other: "Vector") -> bool:
        return self.__gt__(other) or self.__eq__(other)


    def __lt__(self, other: "Vector") -> bool:
        return not self.__ge__(other)


    def __le__(self, other: "Vector") -> bool:
        return not self.__gt__(other)


    def __ne__(self, other: "Vector") -> bool:
        return not self.__eq__(other)


    def __hash__(self) -> int:
        return hash(''.join([str(i) for i in self.lst]))