import collections
import copy

from .Vector import Vector
from .Polynom import Polynom


class Lfsr:
    def __init__(self, init_vect: Vector, init_plnm: Polynom):
        if init_plnm.deg() != len(init_vect):
            raise ValueError("Invalid state & polynomial")
        if init_vect.zero != init_plnm.zero or init_vect.id != init_plnm.id:
            raise ValueError('Vector and polynom have different fields')

        self.plnm = init_plnm
        self.vect = init_vect

    def clock(self):
        res_bit = self.vect.lst[0]
        new_bit = sum([a * b for a, b in zip(self.vect.lst, self.plnm.lst[:-1])], self.vect.zero)
        self.vect.lst = [self.vect.lst[ind] for ind in range(1, len(self.vect))] + [new_bit]
        return res_bit

    def get_cycle_type(self):
        lfsr = copy.deepcopy(self)
        vect_dim = copy.deepcopy(self.vect)
        vect_set = set()
        res_dict = collections.defaultdict(int)

        while vect_dim:
            vect_dim = vect_dim.increment()
            if not vect_dim:
                break
            
            if vect_dim not in vect_set:
                lfsr.vect = copy.deepcopy(vect_dim)
                vect_set.add(lfsr.vect)
                print(f'{len(vect_set)}    {lfsr.vect}')
                lfsr.clock()
                i = 1
                while lfsr.vect != vect_dim:
                    vect_set.add(copy.deepcopy(lfsr.vect))
                    print(f'{len(vect_set)}    {lfsr.vect}')
                    i += 1
                    lfsr.clock()

                print()
                res_dict[i] += 1

        res_dict[1] += 1 # null vect 
        return res_dict
