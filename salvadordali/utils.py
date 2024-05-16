from math import sqrt, factorial
from typing import List

def is_prime(n: int) -> bool:
    if n == 1:
        return True
    
    for i in range(2, int(sqrt(n)) + 1):
        if n % i == 0:
            return False
        
    return True
    

def subsets(arr):
    subs = [[]]
    for i in arr:
        subs += [s + [i] for s in subs]
    return subs


def factorial_coefs(num) -> List[int]:
    res = []
    q = num

    k = 1
    while factorial(k) <= num:
        k += 1
    k -= 1

    for i in range(k, 0, -1):
        fact = factorial(i)
        res.insert(0, q // fact)
        q %= fact

    return res


def base_str(x: int, base: int) -> str:
    res_str = ''
    
    while x > 0:
        res_str = str(x % base) + res_str
        x //= base

    return res_str
