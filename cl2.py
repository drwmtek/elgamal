import socket
import json
import random
p = 0
g = 0
x = 0
y = 0
sock = None
def getPrimeByBits(bitLen):
	bitLow = bitLen
	lower = 2**(bitLow - 1)
	upper = 2**bitLen - 1
	l = getPrime(lower, upper)
	return random.choice(l)

def getPrime(lower, upper):
	l = []
	for num in range(lower,upper + 1):
	   # prime numbers are greater than 1
	   if num > 1:
	       for i in range(2,num):
	           if (num % i) == 0:
	               break
	       else:
	       	l.append(num)
	return l

def main():
	global sock
	sock = socket.socket()
	sock.connect(('localhost', 9090))
	global p
	p = getPrimeByBits(8)
	print('P = {' + str(p) + '}')
	my_str = json.dumps({'cmd': 'CREATE_P', 'data': p})
	sock.send(str.encode(str(my_str)))
	while True:
		data = sock.recv(1024)
		if data:
			res = command(json.loads(data.decode("utf-8")))
			sock.send(str.encode(str(json.dumps(res))))
			if res.get('cmd') == 'EXIT':
				break
	sock.close()

def command(cmd):
	if (cmd.get('cmd') == 'CREATE_G'):
		global g
		g = int(cmd.get('data'))
		print('G = {' + str(g) + '}')
		global x
		x = random.randint(int(1), int(p-1))
		print('X = {' + str(x) + '}')
		return {'cmd': 'CREATE_X', 'data': 'OK'}
	if (cmd.get('cmd') == 'CREATE_Y'):
		global y
		y = (g**x) % p
		print('Y = {' + str(y) + '}')
		print('================')
		print('Public Key (p, g ,y): {' + str(p) + ', ' + str(g) + ', ' + str(y) + '}')
		print('Private Key: {' + str(x) + '}')
		return {'cmd': 'CREATE_Y'}
	if (cmd.get('cmd') == 'MSG'):
		r = int(cmd.get('r'))
		e = cmd.get('e')
		xx = int(input('Enter Private key: '))
		print('R = {' + str(r) + '} ' + 'E = {' + ''.join(e) + '}')
		nList = []
		for c in e:
			cc = (int(c, 16) * r**(p - 1 - xx)) % p
			#cc = int(c, 16) * (r**(x) * r**(-1)) % p
			nList.append(chr(int(cc)))
		print(''.join(nList))
		return send_msg()
	if (cmd.get('cmd') == 'EXIT'):
		return {'cmd': 'EXIT'}


	return {'cmd': 'EMPTY'}

def send_msg():
	k = random.randint(1, p-2)
	print('K = {' + str(k) + '}')
	r = (g**k) % p
	text = input("Text: ")
	if text == 'exit':
		return {'cmd': 'EXIT'}
	else:
		uni = []
		for c in text:
			e = hex((int(ord(c))*(y**k)) % p)
			uni.append(e)
		print('R = {' + str(r) + '} ' + 'E = {' + ''.join(uni) + '}\n=====================================================')
		return {'cmd': 'MSG', 'r': r, 'e': uni}

main()