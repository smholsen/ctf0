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
    return x % m

f = open('AlicePublickey.pem', 'r')
AlicePublicKey = RSA.importKey(f.read())
f.close()
f = open('BobPublickey.pem', 'r')
BobPublicKey = RSA.importKey(f.read())
f.close()

# f = open('Ciphertext.txt', 'r')
# cipherText = f.read()
# f.close()

p = gcd(AlicePublicKey.n, BobPublicKey.n)
print 'P', p
q = AlicePublicKey.n / p
print 'Q', q
lambdaN = lcm(p-1, q-1)
print 'lambdaN', lambdaN
d = modinv(AlicePublicKey.e, lambdaN)
print 'D', d

cipherText = '@\n\xea\xa9\xd9C6\xfd]{:\xaf\xe0\xf6\xe3\x15\xb7\x92i\x0e}\x7f\x8c\xc5\xa9q\xcb\x94\xac{\xad\x0bU\xf5\x8b\xfe\xfbd\xa2\x8e\x19\xa0\xddN\xbb\xfc\xb3W\xcez\xa3\x17\xa8U\n\xf4\xda\xc4\xe1\xa1x"Gw\x00\x12\xd9`;\n\x0c\x94\xef\xe8S\xcd\xa8\x91\xb6\xf08\xeb\n\x8d\xa9u\xec]\xd8\xeb\x98\xf7\x9c\xdbW\xe1h}h\x92\x0f\xa0\x8d\xd8\x0c\x978\xe6\xf7\xc5\xdb\xaa\xca\xf1P\xbf\x1e5\xba\x9f\rc\x92CB\x1eX\x84'
alicesPrivateKey = RSA.construct((AlicePublicKey.n, AlicePublicKey.e, d, p, q, None))
print alicesPrivateKey.decrypt(cipherText)
