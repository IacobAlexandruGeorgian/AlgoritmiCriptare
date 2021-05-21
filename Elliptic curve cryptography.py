# Iacob Alexandru
import collections

def inv(n, q):
    return egcd(n, q)[0] % q

def egcd(a, b):
    s0, s1, t0, t1 = 1, 0, 0, 1
    while b > 0:
        q, r = divmod(a, b)
        a, b = b, r
        s0, s1, t0, t1 = s1, s0 - q * s1, t1, t0 - q * t1
    return s0, t0, a

def sqrt(n, q):
    assert n < q
    for i in range(1, q):
        if i * i % q == n:
            return (i, q - i)
    raise Exception("not found")

Coord = collections.namedtuple("Coord", ["x", "y"])


class EC(object):

    def __init__(self, a, b, q):
        assert a < q and b < q and q > 2
        assert (4 * (a ** 3) + 27 * (b ** 2)) % q != 0
        self.a = a
        self.b = b
        self.q = q
        self.zero = Coord(0, 0)

    def is_valid(self, p):
        if p == self.zero: return True
        l = (p.y ** 2) % self.q
        r = ((p.x ** 3) + self.a * p.x + self.b) % self.q
        print("Punctul:",p,"se afla pe curba")
        return l == r

    def at(self, x):
        assert x < self.q
        ysq = (x ** 3 + self.a * x + self.b) % self.q
        y, my = sqrt(ysq, self.q)
        return Coord(x, y), Coord(x, my)

    def neg(self, p):
        return Coord(p.x, -p.y % self.q)

    def add(self, p1, p2):
        if p1 == self.zero: return p2
        if p2 == self.zero: return p1
        if p1.x == p2.x and (p1.y != p2.y or p1.y == 0):
            return self.zero
        if p1.x == p2.x:
            l = (3 * p1.x * p1.x + self.a) * inv(2 * p1.y, self.q) % self.q
        else:
            l = (p2.y - p1.y) * inv(p2.x - p1.x, self.q) % self.q
        x = (l * l - p1.x - p2.x) % self.q
        y = (l * (p1.x - x) - p1.y) % self.q
        return Coord(x, y)

    def mul(self, p, n):
        r = self.zero
        m2 = p
        while 0 < n:
            if n & 1 == 1:
                r = self.add(r, m2)
            n, m2 = n >> 1, self.add(m2, m2)
        return r

    def order(self, g):
        assert self.is_valid(g) and g != self.zero
        for i in range(1, self.q + 1):
            if self.mul(g, i) == self.zero:
                return i
        raise Exception("Invalid order")

    def numar_puncte(self):
        x = []
        for i in range(0, self.q):
            for j in range(0, self.q):
                if (j**2)%self.q == (i**3 + 1*i +0)%self.q:
                    x.append(Coord(i,j))
        return len(x)

class ElGamal(object):

    def __init__(self, ec, g):
        assert ec.is_valid(g)
        self.ec = ec
        self.g = g
        self.n = ec.order(g)


    def gen(self, priv):
        return self.ec.mul(g, priv)

    def enc(self, plain, pub, r):
        assert self.ec.is_valid(plain)
        assert self.ec.is_valid(pub)
        return (self.ec.mul(g, r), self.ec.add(plain, self.ec.mul(pub, r)))

    def dec(self, cipher, priv):
        c1, c2 = cipher
        assert self.ec.is_valid(c1) and ec.is_valid(c2)
        return self.ec.add(c2, self.ec.neg(self.ec.mul(c1, priv)))

class DiffieHellman(object):

    def __init__(self, ec, g):
        self.ec = ec
        self.g = g
        self.n = ec.order(g)

    def gen(self, priv):
        assert 0 < priv and priv < self.n
        return self.ec.mul(self.g, priv)

    def secret(self, priv, pub):
        assert self.ec.is_valid(pub)
        assert self.ec.mul(pub, self.n) == self.ec.zero
        return self.ec.mul(pub, priv)

class DSA(object):

    def __init__(self, ec, g):
        self.ec = ec
        self.g = g
        self.n = ec.order(g)

    def gen(self, priv):
        assert 0 < priv and priv < self.n
        return self.ec.mul(self.g, priv)

    def sign(self, hashval, priv, r):
        assert 0 < r and r < self.n
        m = self.ec.mul(self.g, r)
        return (m.x, inv(r, self.n) * (hashval + m.x * priv) % self.n)

    def validate(self, hashval, sig, pub):
        assert self.ec.is_valid(pub)
        assert self.ec.mul(pub, self.n) == self.ec.zero
        w = inv(sig[1], self.n)
        u1, u2 = hashval * w % self.n, sig[0] * w % self.n
        p = self.ec.add(self.ec.mul(self.g, u1), self.ec.mul(pub, u2))
        return p.x % self.n == sig[0]


# ECC - cautam un punct pe curba eliptica

# 1. Scriem ecuatia curbei: (y^2 = x^3 + a*x + b) mod q
# 2. Introducem valorile pentru a, b si q
# 3. Cautam doua puncte pe curba eliptica (x,y1), (x,y2) pentru o valoare aleasa x
# 4. Verificam daca acel punct este pe curba astfel:
#   4.1. Daca cele 2 puncte x si y sunt mai mici decat q si sa nu fie (0,0)
#   4.2. Daca y^2 mod q = (x^3 + a*x + b) mod q
#   4.3. Daca multiplicarea punctelor x si y ne va da (0,0)

ec = EC(1, 18, 19)
g, _ = ec.at(7)
assert ec.order(g) <= ec.q
print("Un punct de pe curba eliptica:",g)
# ECC - El Gamal

# 1. Bob genereaza cheia publica si privata:
# - Ia un punct g de pe curba eliptica
# - Multiplica punctul g pentru a gasi toate punctele de pe curba eliptica
# - Alege un alt punct de pe curba eliptica (mesajul clar)
# - Alege o cheie privata (int)
# - Calculeaza cheia publica prin multiplicarea cheii private cu punctul g de pe curba eliptica
# 2. Alice cifreaza mesajul cu cheia publica a lui Bob:
# - Alege un numar aleator secret (int) si il multiplica cu punctul g de pe curba eliptica --> C1
# - Multiplica cheia publica cu numarul aleator si il aduna cu mesajul clar --> C2
# 3. Bob descifreaza mesajul (C1,C2):
# - Scade C2 cu multiplicarea dintre C1 si cheia privata a lui

eg = ElGamal(ec, g)
mapping = [ec.mul(g, i) for i in range(eg.n)]
plain = mapping[7]
print("El Gamal:")
print("Punctele de pe curba eliptica:",mapping)
print("Mesajul clar:",plain)
priv = 5
print("Cheia privata:",priv)
pub = eg.gen(priv)
print("Cheia publica:",pub)
cipher = eg.enc(plain, pub, 15)
decoded = eg.dec(cipher, priv)
assert decoded == plain
assert cipher != pub
print("Mesajul cifrat:",cipher)
print("Mesajul descifrat:",decoded)

# ECC - Diffie-Hellman - protocol de stabilire a cheii

# 1. Alice, Bob si eu alegem un punct g de pe curba eliptica
# 2. Fiecare ne alegem chei private diferite (int)
# 3. Ne calculam fiecare cheia publica prin multiplicarea cheii private cu punctul g
# 4. Ne calculam cheile secrete comune intre noi prin multiplicarea cheii private cu cheia publica a celuilalt

dh = DiffieHellman(ec, g)
print("Diffie-Hellman:")
apriv = 11
print("Cheia privata a lui Alice:",apriv)
apub = dh.gen(apriv)
print("Cheia publica a lui Alice",apub)
bpriv = 3
print("Cheia privata a lui Bob:",bpriv)
bpub = dh.gen(bpriv)
print("Cheia publica a lui Bob",bpub)
cpriv = 7
print("Cheia privata a mea:",cpriv)
cpub = dh.gen(cpriv)
print("Cheia publica a mea:",cpub)
sh_secret_key12=dh.secret(apriv, bpub)
sh_secret_key21=dh.secret(bpriv, apub)
sh_secret_key13=dh.secret(apriv, cpub)
sh_secret_key31=dh.secret(cpriv, apub)
sh_secret_key23=dh.secret(bpriv, cpub)
sh_secret_key32=dh.secret(cpriv, bpub)
# same secret on each pair
assert dh.secret(apriv, bpub) == dh.secret(bpriv, apub)
assert dh.secret(apriv, cpub) == dh.secret(cpriv, apub)
assert dh.secret(bpriv, cpub) == dh.secret(cpriv, bpub)
print("Cheia secreta comuna intre Alice si Bob / Bob si Alice:",sh_secret_key12,sh_secret_key21)
print("Cheia secreta comuna intre Alice si mine / eu si Alice:",sh_secret_key13,sh_secret_key31)
print("Cheia secreta comuna intre Bob si mine / eu si Bob:",sh_secret_key23,sh_secret_key32)

# ECDSA - Elliptic Curve Digital Signature Algorithm
# 1. Bob genereaza cheia publica si semnatura
# - Bob alege un punct g de pe curba eliptica
# - Alege o cheie privata random (int)
# - Genereaza cheia publica prin multiplicarea cheii private cu punctul g
# - Alege o valoare hash (int) pentru mesajul clar (int)
# - Multiplica mesajul clar cu punctul g --> M.x (coordonata x al unui punct de pe curba)
# - Calculeaza S = inv(mesajul clar, lungimea grupului ordonat n) * (valoarea hash + M.x * cheia privata) mod n
# 2. Alice primeste (valoarea hash, semnatura, cheia publica)  si valideaza semnatura
# - Verifica daca M.x si S sunt numere intregi in intervalul [1,n-1]
# - Calculeaza u1 si u2
# - Se foloseste de u1 si u2 pentru a obtine punctul de pe curba eliptica
# - Verifica daca coordonata x al punctului este egala cu M.x

print("Elliptic Curve Digital Signature Algorithm:")
dsa = DSA(ec, g)
priv = 11
print("Cheia privata:",priv)
pub = eg.gen(priv)
print("Cheia publica:",pub)
hashval = 128
r = 7
sig = dsa.sign(hashval, priv, r)
print("Semnatura:",sig)
assert dsa.validate(hashval, sig, pub)

