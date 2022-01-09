import gmpy2
import time
from Crypto.Util.number import inverse
from functools import reduce

def readfile():
    n,e,c = [],[],[]
    for i in range(21):
        f = open('Frames/Frame%d' % i)
        content = f.readline()
        n.append(int(content[:256],16))
        e.append(int(content[256:512],16))
        c.append(int(content[512:],16))
        # n.append(content[:256])
        # e.append(content[256:512])
        # c.append(content[512:])
        f.close
    return n,e,c


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

def exgcd(a, b):
    if b == 0:
        return 1, 0
    x, y = exgcd(b, a % b)
    return y, x - a // b * y

def int2str(a):
    s = ''
    for i in range(8):
        s += chr(a % 256)
        a >>= 8
    s = s[::-1]
    a >>= 352
    return (a & ((1 << 32) - 1)), s

def CRT(a,n):
    sum = 0
    N = reduce(lambda x,y:x*y,n)   # ni 的乘积,N=n1*n2*n3
    for n_i, a_i in zip(n,a):    # zip()将对象打包成元组
        N_i = N // n_i           #Mi=M/ni
        sum += a_i*N_i*inverse(N_i,n_i)   #sum=C1M1y1+C2M2y2+C3M3y3
    return sum % N 


def same_mod(n, e1, c1, e2, c2):
    x, y = exgcd(e1, e2)
    return pow(c1, x, n) * pow(c2, y, n) % n

def same_factor(n1, e1, c1, n2, e2, c2):
    p = gcd(n1, n2)
    q1 = n1 // p
    q2 = n2 // p
    phi1 = (p - 1) * (q1 - 1)
    phi2 = (p - 1) * (q2 - 1)
    d1 = inverse(e1, phi1)
    d2 = inverse(e2, phi2)
    return pow(c1, d1, n1), pow(c2, d2, n2)

if __name__=='__main__':
    n,e,c = readfile()
    m = [0 for i in range(21)]

    print("[+]共模攻击:")
    for i in range(21):
        for j in range(i):
            if n[i] == n[j]:
                m[i] = same_mod(n[i], e[i], c[i], e[j], c[j])
                print(i,',',j, ":", int2str(m[i]))


    print('[+]低加密指数广播攻击:')
    temp1=[]
    temp2=[]
    id = [3, 8, 12, 16, 20]# e = 5的分组
    for i in  id:
        temp1.append(c[i])    
        temp2.append(n[i])
    x = CRT(temp1,temp2)
    tempm = gmpy2.iroot(x,5)[0]
    print(id,':',int2str(tempm))      
 
    print("[+]相同公因数攻击:")
    for i in range(21):
        for j in range(i):
            if gcd(n[i], n[j]) > 1 and n[i] != n[j]:
                m[i], m[j] = same_factor(n[i], e[i], c[i], n[j], e[j], c[j])
                print(i, ":", int2str(m[i]))
                print(j, ":", int2str(m[j]))

    print("[+]模数分解攻击:")



