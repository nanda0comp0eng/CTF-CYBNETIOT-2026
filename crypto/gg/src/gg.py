from Crypto.Util.number import *
from hashlib import sha256
import os

FLAG = b"CYBNETIOT{mudah_kan_yah}"

p = (1 << 127) - 1
order = 2**16

h = 5
g = pow(h, (p - 1) // order, p)

a = getRandomRange(1, order)
b = getRandomRange(1, order)

A = pow(g, a, p)
B = pow(g, b, p)

s = pow(B, a, p)

key = sha256(str(s).encode()).digest()
cipher = bytes(x ^ y for x, y in zip(FLAG, key))

with open("output.txt", "w") as f:
    f.write(f"p = {p}\n")
    f.write(f"g = {g}\n")
    f.write(f"A = {A}\n")
    f.write(f"B = {B}\n")
    f.write(f"ciphertext = {cipher.hex()}\n")
