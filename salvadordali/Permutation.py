import copy
from math import factorial, log
from typing import List

from .utils import factorial_coefs
from .BF import BF
from .GF import GF


class Permutation:
    def __init__(self, vect: List[int]):
        if len(set(vect)) != len(vect) or sum(1 for i in vect if i < 0 or i >= len(vect)) != 0:
            raise ValueError('Invalid vect in permutation init')
        self.lst = vect


    def __invert__(self):
        p = copy.deepcopy(self.lst)
        for i in range(len(self.lst)):
            p[self.lst[i]] = i
        return Permutation(p)


    def __str__(self):
        return (''.join([str(i) + ' ' for i in self.lst]))[:-1]


    def __mul__(self, other: "Permutation"):
        return Permutation([other.func(i) for i in self.lst])


    @staticmethod
    def permut_from_inverse_vect(vect):
        inds = [i for i in range(len(vect))]
        p = []
        for i in range(len(vect)):
            p.insert(0, inds[-vect[-i]])
            inds.pop(-vect[-i])

        return Permutation(p)


    @staticmethod
    def permut_from_ind(ind):
        if ind < 0:
            raise ValueError('Invalid number in setting from index')

        p = [1]
        for i in factorial_coefs(ind):
            p = [i] + [j if j >= i else j for j in p]

        return Permutation(p)


    @staticmethod
    def cycle_permut(n, k, d):
        if k < 1 or n < 1 or k > n:
            raise ValueError('Invalid args in cycle permutation')
        d %= k
        id = [i for i in range(n)]
        return Permutation(id[:k][d:] + id[:k][:d] + id[k:])


    def func(self, arg):
        if arg > len(self.lst) or arg < 1:
            raise ValueError('Invalid argument in permutation')
        
        return self.lst[arg]


    def ind(self):
        if len(self.lst) == 1:
            return 0
        
        return (self.lst[0]) * factorial(len(self.lst) - 1) + Permutation(
            [i if i > self.lst[0] else i for i in self.lst[1:]]).ind()


    def invers_vect(self):
        return [sum(1 for i in self.lst[:self.lst.index(x)] if i > x) for x in self.lst]


    def lexicographical_next(self):
        p = copy.deepcopy(self.lst)
        k = -1
        for i in range(len(p) - 2, -1, -1):
            if p[i] < p[i + 1]:
                k = i
                break
        if k == -1:
            return None
        j = p.index(min([i for i in p[k + 1:] if p[k] < i]))
        p[k], p[j] = p[j], p[k]
        return Permutation(p[:k + 1] + p[k + 1:][::-1])


    def decompose_cycle(self):
        n = len(self.lst)
        p_list = []

        for i in range(n, 1, -1):
            q = (~self).lst[i - 1]
            for k in range(n, i, -1):
                q = p_list[n - k].lst[q - 1]
            p_list.append(Permutation.cycle_permut(n, i, i - q))

        return p_list
    
    
        
        
