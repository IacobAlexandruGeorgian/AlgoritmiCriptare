# Iacob Alexandru - Rabin
def gcdEuclid(p,q):
    if p == 0:
        return q,0,1
    gcd,a1,b1 = gcdEuclid(q%p,p)
    a = b1 - (q//p) * a1
    b = a1
    return gcd,a,b

def Rabin_cifrare(p, q, mesaj):
    N = p*q
    pbl_key = N
    prv_key = (p,q)
    mesaj_bin = ''.join(format(ord(i), 'b') for i in mesaj)
    print(mesaj_bin)
    mesaj_int = int(mesaj_bin,2)
    print(mesaj_int)
    c = pow(mesaj_int,2) % N
    print(c)
    return c, mesaj_bin

def descifrare(c, p, q, mesaj_bin):
    n = p*q
    gcd,a,b = gcdEuclid(p,q)
    print("a*p+b*q =",a*p+b*q)
    r = pow(int(c),int((p+1)/4),int(p))
    s = pow(int(c),int((q+1)/4),int(q))
    x = int((a * p * s + b * q * r) % n)
    y = int((a * p * s - b * q * r) % n)
    radacini = [x, -x % n, y, -y % n]
    m = 0
    for i in radacini:
        nr_bin = format(i,"b")
        print(nr_bin)
        if(nr_bin == mesaj_bin):
            m = nr_bin

    print(m)
    mesaj_descifrat_int = int(m,2)
    print(mesaj_descifrat_int)

    return mesaj_descifrat_int

mesaj = "A"
p, q = 11, 19
mesaj_cifrat, mesaj_bin = Rabin_cifrare(p, q, mesaj)
mesaj_descifrat = descifrare(mesaj_cifrat,p,q, mesaj_bin)
print("mesaj: ",mesaj)
print("mesaj cifrat: ",mesaj_cifrat)
print("mesaj descifrat: ",mesaj_descifrat)




