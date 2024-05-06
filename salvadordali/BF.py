import math
import copy
from typing import List, Tuple

from .GF import GF
from .Polynom import Polynom
from .utils import subsets


class BF:
    def __init__(self, vect: List[GF]):
        if len(vect) < 1:
            raise ValueError('Vector size < 1')
        if not math.log(len(vect), 2).is_integer():
            raise ValueError('Invalid vector. Size must be = 2^(args number)')
        for i in vect:
            if isinstance(i, GF):
                if i.pow != 2:
                    raise ValueError('Not GF(2) elem in vector')
            else:
                raise ValueError('Not GF(2) elem in vector')

        self.lst: List[GF] = vect
        self.args_num: int = int(math.log(len(vect), 2))


    def __str__(self) -> str:
        return ''.join([format(i, f'>0{self.args_num}b') + ' ' + str(self.lst[i]) + '\n' for i in range(len(self.lst))])
    

    def __add__(self, other: "BF") -> "BF":
        if len(self.lst) != len(other.lst):
            raise ValueError("Boolean functions must be same size")
        
        return BF([a + b for a, b in zip(self.lst, other.lst)])


    def func(self, args):
        if len(args) != self.args_num:
            raise ValueError('Invalid args number')
        for i in args:
            if isinstance(i, GF):
                if i.pow != 2:
                    raise ValueError('Not GF(2) elem in vector')
            else:
                raise ValueError('Not GF(2) elem in vector')

        return self.lst[int(''.join([str(i.val) for i in args]), 2)]
    

    @classmethod
    def _zhegalcin_trans(cls, lst: List[GF]) -> List[GF]:
        length = len(lst)

        if length == 1:
            return lst
    
        l_lst = lst[:length // 2]
        r_lst = lst[length // 2:]

        r_lst = [l + r for l, r in zip(l_lst, r_lst)]

        return cls._zhegalcin_trans(l_lst) + cls._zhegalcin_trans(r_lst)


    def zhegalcin_plnm(self) -> List[GF]:
        return self._zhegalcin_trans(self.lst)
    

    def zhegalcin_plnm_str(self) -> str:
        zhegalcin_plnm = self.zhegalcin_plnm()
        monoms_list = []

        if zhegalcin_plnm[0].val == 1:
            monoms_list.append('1')

        for i in range(1, len(zhegalcin_plnm)):
            if zhegalcin_plnm[i].val == 1:
                vect = format(i, 'b').zfill(self.args_num)
                monom = '⋅'.join([f'x{j + 1}' for j in range(len(vect)) if vect[j] == '1'])
                monoms_list.append(monom)

        return ' ⨁ '.join(sorted(monoms_list, key=lambda x: (len(x), x), reverse=False))


    def deg(self):
        res = 0
        zheg_plnm = self.zhegalcin_plnm()
        for i in range(len(zheg_plnm)):
            if zheg_plnm[i].val == 1:
                res = max(res, format(i, 'b').count('1'))
        return res


    def weight(self):
        return self.lst.count(GF(2, 1))
    

    def hamming_dist(self, other: "BF") -> int:
        if len(self.lst) != len(other.lst):
            raise ValueError("Functions must have same size")
        
        return sum(1 if self.lst[i] != other.lst[i] else 0 for i in range(len(self.lst)))
    


    def fixed_func(self, vals, inds):
        if len(vals) != len(inds):
            raise ValueError('Different size of values arr and indexes arr')
        for i in vals:
            if isinstance(i, GF):
                if i.pow != 2:
                    raise ValueError('Not GF(2) elem in values arr')
            else:
                raise ValueError('Not GF(2) elem in values arr')

        for i in inds:
            if i < 0 or i >= self.args_num:
                raise ValueError('Invalid index in indexes arr')

        func_vals = []
        for i in range(len(self.lst)):
            arg = format(i, f'>0{self.args_num}b')
            if math.prod([int(arg[inds[j]] == str(vals[j])) for j in range(len(inds))]) == 1:
                func_vals.append(self.lst[i])

        return BF(func_vals)


    def analytic_struct(self):
        a = [i for i in range(self.args_num)]

        for inds in sorted([i for i in subsets(a) if 0 < len(i) < self.args_num], key=lambda x: (len(x), x[0])):
            print(f'deg f{[i + 1 for i in inds]}: ')
            for val in range(len(self.lst)):
                print(self.fixed_func([GF(2, int(format(val, f'>0{self.args_num}b')[i])) for i in inds], inds).deg(),
                      end='  ')
            print()


    def weight_struct(self):
        a = [i for i in range(self.args_num)]

        for inds in sorted([i for i in subsets(a) if 0 < len(i) < self.args_num], key=lambda x: (len(x), x[0])):
            print(f'weight f{[i + 1 for i in inds]}: ')
            for val in range(len(self.lst)):
                print(self.fixed_func([GF(2, int(format(val, f'>0{self.args_num}b')[i])) for i in inds], inds).weight(),
                      end='  ')
            print()


    def fourier_trans(self, arr):
        if len(arr) == 1:
            return arr

        l_arr = arr[:len(arr) // 2]
        r_arr = arr[len(arr) // 2:]

        l_arr, r_arr = [a + b for a, b in zip(l_arr, r_arr)], [a - b for a, b in zip(l_arr, r_arr)]

        return self.fourier_trans(l_arr) + self.fourier_trans(r_arr)
    

    def walsh_hadamard_trans(self) -> List[int]:
        return self.fourier_trans([int(math.pow(-1, int(i))) for i in self.lst])
    

    def nl(self) -> int:
        return int(pow(2, self.args_num - 1) - max(self.walsh_hadamard_trans(), key=abs) / 2)
    

    def linear_approximations_predominances(self) -> List[float]:
        return [val / pow(2, self.args_num + 1) for val in self.walsh_hadamard_trans()]
    

    def best_linear_approximation(self) -> Tuple[int, float]:
        lap = self.linear_approximations_predominances()
        max_val = max(lap, key=abs)
        max_ind = lap.index(max_val)

        return max_ind, max_val

