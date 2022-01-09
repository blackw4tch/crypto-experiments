
import random

from base64 import b64decode
from Crypto.Cipher import AES

 
 
def padding(s: bytes):
	r = (16 - len(s) % 16) % 16
	return s + r.to_bytes(1, 'big') * r

def f1(s: bytes, aes, pre):
	c = b'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg' + \
	b'aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq' + \
	b'dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg' + \
	b'YnkK'
	c = b64decode(c)
	s = padding(pre + s + c)
	return aes.encrypt(s)
 
def main(aes, pre):
	s = f1(b'', aes, pre)
	last = s[:16]
	pre_len = 0
	for i in range(1, 16):
		s = f1(b'a' * i, aes, pre)
		if s[:16] == last:
			pre_len = 16 - i + 1
			break
		last = s[:16]
	
	print(pre_len)
	max_len = 1024
	m = b''
	while True:
		blank = b'\x00' * (max_len - 1 - pre_len - len(m))
		for i in range(1, 256):
			s = blank + m + i.to_bytes(1, 'big')
			t = blank
			if f1(s, aes, pre)[:max_len] == f1(t, aes, pre)[:max_len]:
				m = m + i.to_bytes(1, 'big')
				break
		print(m.decode())
 
 
if __name__ == '__main__':
	pre_len = random.randint(1, 16)
	print(pre_len)
	pre = random.randbytes(pre_len)
	key = random.randbytes(16)
	iv = random.randbytes(16)
	aes = AES.new(key, AES.MODE_ECB)
	main(aes, pre)

