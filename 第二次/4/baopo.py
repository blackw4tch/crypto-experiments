import time
import hashlib

chars = 'QWINqwin%(*=58'
chars
miwen="67ae1a64661ac8b4494666f58c4822408dd0a3e4"
strings = []
time1=time.time()

def fun(prefix):
    for x in chars:
        mingwen=prefix+x
        if (hashlib.sha1(mingwen.encode()).hexdigest() == miwen):
            time2 = time.time()
            print(mingwen)
            print(time2 - time1)
            exit()
        if len(prefix + x) < 8:
            fun(prefix + x)
fun('')


