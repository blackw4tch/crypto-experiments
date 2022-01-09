from Crypto.Cipher import AES
import random

def padding(s: bytes):
	r = (16 - len(s) % 16) % 16
	return s + r.to_bytes(1, 'big') * r
 
 
def string(s: str, aes):
	if ";" in s or "=" in s:
		exit(0)
	s = "comment1=cooking%20MCs;userdata=" + \
		s + \
		";comment2=%20like%20a%20pound%20of%20bacon"
	return aes.encrypt(padding(s.encode()))
 
 
def byte(s: bytes, aes):
	s = aes.decrypt(s)
	print(s)
	return b';admin=true;' in s
 
	
if __name__ == '__main__':
	key = random.randbytes(16)
	iv = random.randbytes(16)
	aes1 = AES.new(key, AES.MODE_CBC, iv)
	aes2 = AES.new(key, AES.MODE_CBC, iv)
	
	payload = '\x00' * 32
	c = string(payload, aes1)
	m = b';admin=true;' + b'\x00' * 4
	t = b''
	for i in range(32, 48):
		t = t + (m[i - 32] ^ c[i]).to_bytes(1, 'big')
	c = c[:32] + t + c[48:]
	
	print(byte(c, aes2))