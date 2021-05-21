import math


def modInverse(a, m):
    m0 = m
    y = 0
    x = 1

    if (m == 1):
        return 0

    while (a > 1):
        q = a // m # coeficient
        t = m # reminder
        m = a % m
        a = t
        t = y
        y = x - q * y # modific x & y dupa fiecare iteratie
        x = t
    if (x < 0): # fac x pozitiv
        x = x + m0

    return x

def compute_lcm(x, y):

   if x > y:
       greater = x
   else:
       greater = y

   while(True):
       if((greater % x == 0) and (greater % y == 0)):
           lcm = greater
           break
       greater += 1

   return lcm

def RSA1(criptez, p, q):
    N = p * q
    FI = compute_lcm(p-1,q-1)
    print(FI)
    e = 3
    d = modInverse(e, FI)
    criptat = pow(criptez,e) % N
    decriptat = pow(criptat, d) % N
    return d, criptat, decriptat

criptez = 25 # 8 digits
d, criptat, decriptat = RSA1(criptez,53,191) # 317,9817
print("d = ", d)
print("criptez: ", criptez)
print("criptat: ", criptat)
print("decriptat: ", decriptat)


