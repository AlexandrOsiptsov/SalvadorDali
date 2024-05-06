from typing import List, Tuple, Callable
from math import log2

from .GF import GF
from .Vector import Vector
from .BF import BF


class BoolSubstitution:
    def __init__(self, sub: List[Vector[GF]]):
        if not isinstance(sub[0][0], GF):
            raise TypeError("Invalid vector elem in substitution")
        
        if not sub[0][0].pow == 2:
            raise ValueError("Vectors must be from boolean ring")
        
        if not log2(len(sub)).is_integer():
            raise ValueError("Boolean substitution must have 2^n vectors")
               
        self.sub = sub
        self.n = int(log2(len(sub)))
        self.m = len(sub[0])


    @staticmethod
    def from_int_list(lst: List[int]) -> "BoolSubstitution":
        bits_num = log2(len(lst))

        if not bits_num.is_integer():
            raise ValueError("Boolean substitution must have 2^n vectors")
        bits_num = int(bits_num)
    
        sub = [Vector([GF(2, (lst[i] >> j) & 1) for j in range(bits_num)], GF(2, 0), GF(2, 1)).reversed() for i in range(len(lst))]

        return BoolSubstitution(sub)
    

    def func(self, x: Vector[GF]) -> Vector[GF]:
        if x[0].pow != 2:
            raise ValueError("Vectors must be from boolean ring")
        
        if len(x) != self.n:
            raise ValueError("Invalid vector size")

        return self.sub[x.gf_ind()]
    

    def func_int(self, x: int) -> Vector[GF]:
        if not 0 <= x < len(self.sub):
            raise ValueError("Invalid x")
        
        return self.sub[x]
    

    def dec_list(self) -> List[int]:
        return [sum([self.sub[i].reversed()[j].val * (2 ** j) for j in range(self.m)]) for i in range(len(self.sub))]
    

    def __str__(self) -> str:
        width = 2

        inds = ' '.join([str(ind).zfill(width) for ind in range(len(self.sub))])

        res: str = inds + '\n'

        for i in range(len(self.sub)):
            int_val = sum([self.sub[i].reversed()[j].val * (2 ** j) for j in range(self.m)])
            res += str(int_val).zfill(width) + ' '

        return res
    

    def str_bin_colums(self) -> str:
        bits_num = int(log2(len(self.sub)))
        return '\n'.join([format(i, 'b').zfill(bits_num) + ' -> ' + ''.join([str(self.sub[i][j].val) for j in range(len(self.sub[i]))]) for i in range(len(self.sub))])


    def coord_bf_list(self) -> List[BF]:
        return [BF([self.sub[i][j] for i in range(len(self.sub))]) for j in range(self.m)]
    

    def coord_bf_combs_list(self) -> List[BF]:
        res_list = []

        coord_bf_list = self.coord_bf_list()
        zero_bf = BF([GF(2, 0) for _ in range(len(self.sub))])
        bits_num = len(coord_bf_list)

        for i in range(pow(2, bits_num)):
            vect = format(i, 'b').zfill(bits_num)
            bf = sum([coord_bf_list[j] for j in range(bits_num) if vect[j] == '1'], zero_bf)
            res_list.append(bf)

        return res_list


    def deg(self) -> int:
        return min([bf.deg() for bf in self.coord_bf_combs_list()[1:]])
    

    def nl(self) -> int:
        return min([bf.nl() for bf in self.coord_bf_combs_list()[1:]])
    

    def linear_approximations_predominances_table(self) -> List[List[float]]:
        res_table: List[List[float]] = [bf.linear_approximations_predominances() for bf in self.coord_bf_combs_list()]
        res_table = [[res_table[k][j] for k in range(len(res_table))] for j in range(len(res_table[0]))]
        return res_table
    

    def best_linear_approximation(self) -> Tuple[int, int, float]:
        lap_table = self.linear_approximations_predominances_table()

        max_a = 1
        max_b = 1
        max_elem = lap_table[max_a][max_b]

        for i in range(1, len(lap_table)):
            for j in range(1, len(lap_table[i])):
                if abs(lap_table[i][j]) > abs(max_elem):
                    max_elem = lap_table[i][j]
                    max_a = i
                    max_b = j

        return max_a, max_b, max_elem
    

    def difference_value(
            self,
            a: Vector[GF],
            b: Vector[GF],
            op1: Callable[[Vector[GF], Vector[GF]], Vector[GF]] = Vector.__add__,
            op2: Callable[[Vector[GF], Vector[GF]], Vector[GF]] = Vector.__add__
    ):
        if len(a.lst) != self.n:
            raise ValueError("Invalid vector A")
        
        if len(b.lst) != self.m:
            raise ValueError("Invalid vector B")
        
        res_sum = 0

        for x in range(len(self.sub)):
            x_vect = Vector.from_int(x, 2, self.n)

            if self.func(op1(x_vect, a)) == op2(self.func(x_vect), b):
                res_sum += 1

        return res_sum


    def differences_table(
            self,
            op1: Callable[[Vector[GF], Vector[GF]], Vector[GF]] = Vector.__add__,
            op2: Callable[[Vector[GF], Vector[GF]], Vector[GF]] = Vector.__add__
    ) -> List[List[int]]:
        
        return [[self.difference_value(Vector.from_int(i, 2, self.n), Vector.from_int(j, 2, self.m), op1, op2) 
                 for j in range(pow(2, self.m))] for i in range(pow(2, self.n))]
        

    def R(self,
          op1: Callable[[Vector[GF], Vector[GF]], Vector[GF]] = Vector.__add__,
          op2: Callable[[Vector[GF], Vector[GF]], Vector[GF]] = Vector.__add__
    ) -> Tuple[int, int, int]:
        
        lap_table = self.differences_table(op1, op2)

        max_a = 1
        max_b = 1
        max_elem = lap_table[max_a][max_b]
    
        for i in range(1, len(lap_table)):
            for j in range(1, len(lap_table[i])):
                if abs(lap_table[i][j]) > abs(max_elem):
                    max_elem = lap_table[i][j]
                    max_a = i
                    max_b = j

        return max_a, max_b, max_elem

    
    

    

            
        

        



    

