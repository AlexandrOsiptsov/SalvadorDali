from re import M
from salvadordali import Polynom, Vector, GF, Matrix


GF2_ZERO = GF(2, 0)
GF2_NEUT = GF(2, 1)

p1 = Polynom(Vector([GF(2, i) for i in [1,0,1,1,1,0,0,0,1]], GF2_ZERO, GF2_NEUT), GF2_ZERO, GF2_NEUT)



p = Matrix(1, 4, [[GF(2, i) for i in [1,1,1,1]]])

m = Matrix(4, 4, 
    [
        [GF(2, i) for i in [0,0,0,1]],
        [GF(2, i) for i in [1,0,0,1]],
        [GF(2, i) for i in [0,1,0,0]],
        [GF(2, i) for i in [0,0,1,0]]
    ]
)

m_char = m.char_eq()

for i in range(1, 17):
    res = m ** i
    print(f'{str(i).zfill(2)}:       \n{res}')
    print(f'res.char_eq()   :   {res.char_eq()}')
    print()
    

# p = Matrix(1, 4, [[GF(2, i) for i in [1,1,1,1]]])
# print()
# deg = 3
# print(f'p * A^{deg} = {p * (m ** deg)}')

# print()
# print()

# i = 1
# m_it = m ** i
# while True:
#     print(f'{i}:')
#     print(m_it)
#     print('ppp', p * m_it)
#     m_it *= m
#     # print()
#     i += 1
#     if m_it == m: break