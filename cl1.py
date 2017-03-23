import socket
import json
import random
import sys
p = 0
g = 0
x = 0
y = 0

def gcd(a,b):
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a

def primitive_root(modulo):
    required_set = set(num for num in range (1, modulo) if gcd(num, modulo) == 1)
    for g in range(1, modulo):
        actual_set = set(pow(g, powers) % modulo for powers in range (1, modulo))
        if required_set == actual_set:
            return g

def main():
	sock = socket.socket()
	sock.bind(('', 9090))
	sock.listen(1)
	conn, addr = sock.accept()
	print ('Client connected:' + str(addr))

	while True:
	    data = conn.recv(1024)
	    if data:
	    	res = command(json.loads(data.decode("utf-8")))
	    	conn.send(str.encode(str(json.dumps(res))))
	    	if(res.get('cmd') == 'EXIT'):
	    		break
	conn.close()
	sock.close()


def command(cmd):
	if (cmd.get('cmd') == 'CREATE_P'):
		global p
		p = int(cmd.get('data'))
		print('P = {' + str(p) + '}')
		global g
		g = primitive_root(p)
		print('G = {' + str(g) + '}')
		return {'cmd': 'CREATE_G', 'data': g}
	if (cmd.get('cmd') == 'CREATE_X'):
		global x
		x = random.randint(int(1), int(p - 1))
		print('X = {' + str(x) + '}')
		global y
		y = (g**x) % p
		print('Y = {' + str(y) + '}')
		print('================')
		print('Public Key (p, g ,y): {' + str(p) + ', ' + str(g) + ', ' + str(y) + '}')
		print('Private Key: {' + str(x) + '}')
		return {'cmd': 'CREATE_Y'}
	if (cmd.get('cmd') == 'CREATE_Y'):
		return send_msg()
	if (cmd.get('cmd') == 'MSG'):
		r = int(cmd.get('r'))
		e = cmd.get('e')
		xx = int(input('Enter Private key: '))
		print('R = {' + str(r) + '} ' + 'E = {' + ''.join(e) + '}')
		nList = []
		for c in e:
			#cc = int(c, 16) * (r**(xx) * r**(-1)) % p
			cc = (int(c, 16) * r**(p - 1 - xx)) % p
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