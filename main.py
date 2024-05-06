"""
Выводит на экран некоторую информацию по заданной подстановке
"""

import random
from tabulate import tabulate

from salvadordali import GF, BF, Permutation, Vector, BoolSubstitution



int_list = [8, 1, 15, 9, 13, 6, 7, 12, 0, 14, 5, 4, 10, 11, 2, 3]
# random.shuffle(int_list) # получаем случайное биективное отображение
S = BoolSubstitution.from_int_list(int_list)

# Пример подстановки из {0, 1} ^ (3) -> {0, 1} ^ (2)
G = BoolSubstitution([Vector([GF(2, i) for i in vals], GF(2, 0), GF(2, 1)) 
                      for vals in [[0, 1], [1, 1], [0, 0], [1, 0], [0, 1], [1, 0], [0, 0], [1, 1]]])

print()
print('Подстановка S:')
print(tabulate([S.dec_list()], headers=range(len(S.sub)), tablefmt="rounded_outline"), '\n')

print('Координатные функции подстановки S:\n')
for ind, bf in enumerate(S.coord_bf_list()):
    max_la_ind, max_la = bf.best_linear_approximation()

    print(f"   =============================== S{ind + 1} ==============================")
    print(f"   Столбец значений ф-ции:      ", *bf.lst)
    print(f"   Коэфф-ы мн-на Жегалкина:     ", *bf.zhegalcin_plnm())
    print(f"   Мн-н Жегалкина:              ", bf.zhegalcin_plnm_str())
    print(f"   Степень ф-ции deg(S{ind + 1}):       ", bf.deg())
    print(f"   Степень нелинейности nl(S{ind + 1}): ", bf.nl())
    print(f"   Лучшее преобладание ЛА:      ", max_la, f"({format(max_la_ind, 'b').zfill(len(S.sub[0]))} = {max_la_ind})")
    print()

print("Степень подстановки deg(S) = ", S.deg())
print("Степень нелинейности подстановки nl(S) = ", S.nl(), '\n')



la_a, la_b, max_la = S.best_linear_approximation()
print(f"Лучшее преобладание: {max_la}  ({la_a}, {la_b}  =  {format(la_a, 'b').zfill(len(S.sub[0]))}, {format(la_b, 'b').zfill(len(S.sub[0]))})")
print("Таблица преобладаний линейных аппроксимаций подстановки S:")
print(tabulate(
        S.linear_approximations_predominances_table(), 
        headers=range(pow(2, len(S.sub[0]))), 
        showindex="always",
        tablefmt="rounded_outline"
), "\n\n")


for op1, op2, op1_name, op2_name in [
    (Vector.__add__, Vector.__add__, '⨁', '⨁'),
    (Vector.__add__, Vector.gf_ring_add, '⨁', '⊞'),
    (Vector.gf_ring_add, Vector.__add__, '⊞', '⨁'),
    (Vector.gf_ring_add, Vector.gf_ring_add, '⊞', '⊞'),
]:
    r_a, r_b, max_r = S.R(op1, op1)
    print(f"Значение R(S) (для {op1_name} , {op2_name} ) = {max_r}  ({r_a}, {r_b}  =  {format(r_a, 'b').zfill(len(S.sub[0]))}, {format(r_b, 'b').zfill(len(S.sub[0]))})")
    print(f"Таблица разностей подстановки S (для {op1_name} , {op2_name} ):")
    print(tabulate(
        S.differences_table(op1, op2),
        headers=range(pow(2, len(S.sub[0]))), 
        showindex="always",
        tablefmt="rounded_outline"
    ))
    print()