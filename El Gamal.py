# Iacob Alexandru - El Gamal

# Algoritmul El Gamal utilizat in cod
# 1. Bob genereaza cheia publica si privata:
# - Bob alege un grup ciclic Fq si un numar q
# - Din grupul ciclic alege un element la intamplare g si un element a astfel incat gcd(a,q)=1
# - Calculeaza h = g^a mod q
# - Bob trimite catre Alice cheia publica (Fq,h,g,q) si pastreaza cheia lui privata a
# 2. Alice cifreaza mesajul cu cheia publica a lui Bob:
# - Alice selecteaza un element k din grupul ciclic Fq astfel incat gcd(k,q)=1
# - Calculeaza p1=g^k mod q si s1=h^k mod q
# - Calculeaza p2=s1*M mod q (M este mesajul)
# - Trimite catre Bob (p1,p2) --> criptograma
# 3. Bob descifreaza mesajul:
# - Bob calculeaza s2=p^a mod q
# - Imparte p2 la s2 ca sa obtina mesajul M clar

import random
from math import pow

a = random.randint(2, 10)

def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b;
    else:
        return gcd(b, a % b)

def gen_key(q):
    key = random.randint(pow(10, 20), q)
    while gcd(q, key) != 1:
        key = random.randint(pow(10, 20), q)
    return key

def power(a, b, c):
    x = 1
    y = a
    while b > 0:
        if b % 2 == 0:
            x = (x * y) % c;
        y = (y * y) % c
        b = int(b / 2)
    return x % c

def encrypt(msg, q, h, g):
    en_msg = []
    k = gen_key(q)  # Private key for sender
    s = power(h, k, q)
    p = power(g, k, q)
    for i in range(0, len(msg)):
        en_msg.append(msg[i])
    print("g^k used : ", p)
    print("h^k used : ", s)
    for i in range(0, len(en_msg)):
        en_msg[i] = s * ord(en_msg[i])
    return en_msg, p

def decrypt(en_msg, p, key, q):
    dr_msg = []
    h = power(p, key, q)
    for i in range(0, len(en_msg)):
        dr_msg.append(chr(int(en_msg[i] / h)))
    return dr_msg

msg = "ABCabc"
print("Original Message :", msg)
q = random.randint(pow(10, 20), pow(10, 50))
g = random.randint(2, q)
key = gen_key(q)
h = power(g, key, q)
print("g used : ", g)
print("g^a used : ", h)
en_msg, p = encrypt(msg, q, h, g)
dr_msg = decrypt(en_msg, p, key, q)
dmsg = ''.join(dr_msg)
print("Decrypted Message :", dmsg);


