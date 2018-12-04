import utility
from SeparatePrograms.suma_multiplicacion import *
import functools

def xgcd(b, a):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return b, x0, y0

def extended_euclidean(b, a):
    x0, x1, y0, y1 = BitArray(bin = "0b1"),\
                     BitArray(bin = "0b0"),\
                     BitArray(bin = "0b0"),\
                     BitArray(bin = "0b1")
    while a.int != 0:
        print("dividend", b.bin)
        print("divisor", a.bin)
        temp = a
        q,a = division(b,a)
        #q = BitArray(bin = bin(b.uint // a.uint))
        #a = BitArray(bin = bin(b.uint % a.uint))
        print("quotient", q.bin)
        print("rem", a.bin)
        b = temp
        x0, x1 = x1, add(x0, polynomial_product(q, x1))
        y0, y1 = y1, add(y0, polynomial_product(q, y1))
        print("x0", x0)
        print("x1", x1)
        print("y0", y0)
        print("y1", y1)
        #x0, x1 = x1, x0 - q * x1
        #y0, y1 = y1, y0 - q * y1
    return b.bin, x0.bin, y0.bin


print(extended_euclidean(BitArray(bin = "0b101011"),
                                 BitArray(bin = "0b101")))