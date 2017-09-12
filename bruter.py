import numpy as np
from fractions import gcd
from Crypto.PublicKey import RSA


def lcm(a, b):
    return a * b / gcd(a, b)


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b%a,a)
    return (g, x - (b//a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x%m

f = open('AlicePublickey.pem', 'r')
AlicePublicKey = RSA.importKey(f.read())
f.close()
f = open('BobPublickey.pem', 'r')
BobPublicKey = RSA.importKey(f.read())
f.close()
f = open('Ciphertext.txt', 'r')
cipherText = f.read()
f.close()

p = gcd(AlicePublicKey.n, BobPublicKey.n)
print 'P', p
q = AlicePublicKey.n / p
print 'Q', q
lambdaN = lcm(p-1, q-1)
print 'lambdaN', lambdaN
d = modinv(AlicePublicKey.e, lambdaN)
print 'D', d

alicesPrivateKey = RSA.construct((AlicePublicKey.n, AlicePublicKey.e, d, p, q, None))
print alicesPrivateKey.decrypt(cipherText)
