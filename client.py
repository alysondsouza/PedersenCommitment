from socket import create_connection
from ssl import SSLContext, PROTOCOL_TLS_CLIENT
import random
import sympy            #pip install sympy

hostname='example.org'
ip = '127.0.0.1'
port = 8443
context = SSLContext(PROTOCOL_TLS_CLIENT)
context.load_verify_locations('cert.pem')

with create_connection((ip, port)) as client:
    with context.wrap_socket(client, server_hostname=hostname) as tls:
        print("[ALICE]")
        print(f'Connected using {tls.version()}\n')

        print(f'Alice starts the game:')

        p = sympy.randprime(1, 10000)
        q = 2*p + 1
        g = random.randrange(1, q-1)
        s = random.randrange(1, q-1)
        h = pow(g, s, q) # h = g^s (mod p)
        r = random.randrange(1, q-1)

        print(f'P: {p}')
        print(f'Q: {q}')
        print(f'G: {g}')
        print(f'S: {s}')
        print(f'H: {h}')
        print(f'R: {r}\n')

        tls.sendall(bytes(str(p),'utf-8'))
        tls.sendall(bytes(str(q),'utf-8'))
        tls.sendall(bytes(str(g),'utf-8'))
        tls.sendall(bytes(str(h),'utf-8'))

        alice_num = random.randrange(1,6)
        print(f'Alice number is: {alice_num}')

        # c = g^m*h^r (mod p)
        alice_commitment = str((pow(g, alice_num, q) * pow(h ,r, q)) % q)
        #print(f'hash: {alice_hash_message}')

        print(f'Alice\'s commitment: {alice_commitment}')

        tls.sendall(bytes(alice_commitment,'utf-8'))
        print(f'Alice sends her commitment to Bob. \n')

        bob_number_received = tls.recv(1024).decode('utf-8')
        print(f'Alice receives Bob\'s number: {bob_number_received}\n')

        tls.sendall(bytes(str(alice_num),'utf-8'))
        print(f'Alice reveals her number to Bob: {alice_num}')

        tls.sendall(bytes(str(r),'utf-8'))
        print(f'Alice reveals her random number to Bob: {r}\n')

        #alice_hash_message = hashlib.sha256(alice_num.encode('utf-8')).hexdigest()
