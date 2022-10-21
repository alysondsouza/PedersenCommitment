from socket import socket, AF_INET, SOCK_STREAM
from ssl import SSLContext, PROTOCOL_TLS_SERVER
import random

ip = '127.0.0.1'
port = 8443
context = SSLContext(PROTOCOL_TLS_SERVER)
context.load_cert_chain('cert.pem', 'key.pem')

def start():
    with socket(AF_INET, SOCK_STREAM) as server:
        server.bind((ip, port))
        server.listen(1)
        with context.wrap_socket(server, server_side=True) as tls:
            connection, address = tls.accept()
            print(f'Connected at {address}\n')

            conn = True
            while conn:
                print(f'Alice starts the game:')

                p = connection.recv(1024).decode('utf-8')
                q = connection.recv(1024).decode('utf-8')
                g = connection.recv(1024).decode('utf-8')
                h = connection.recv(1024).decode('utf-8')

                print(f'P: {p}')
                print(f'Q: {q}')
                print(f'G: {g}')
                print(f'H: {h}\n')

                commitment_received = connection.recv(1024).decode('utf-8')
                print(f'Bob receives a commitment from Alice: {commitment_received}\n')

                bob_num = str(random.randrange(1,6))
                print(f'Bob number is: {bob_num}')

                connection.sendall(bytes(bob_num,'utf-8'))
                print(f'Bob send his number to Alice.\n')

                alice_number_received = connection.recv(1024).decode('utf-8')
                print(f'Alice reveals her number: {alice_number_received}')

                alice_random_number_received = connection.recv(1024).decode('utf-8')
                print(f'Alice reveal her random number: {alice_random_number_received}\n')

                #Correct Number
                print(f'Bob can verify the message Alice sent \"{alice_number_received}\" is the same that Alice has commited:', end = ' ')
                match = verify(q, g, h, commitment_received, alice_number_received, alice_random_number_received)
                print("True\n") if match == True else print("False\n")

                #False Number
                print(f'If Alice tries to cheat sending a different message: \"{int(alice_number_received) + 1}\", Bob can verify the message is:', end = ' ')
                match = verify(q, g, h, commitment_received, 7, alice_random_number_received)
                print("True\n") if match == True else print("False\n")

                conn = False
                input()

            connection.close()

def verify(qx, gx, hx, cx, mx, *r):
    q = int(qx)
    g = int(gx)
    h = int(hx)
    c = int(cx)
    m = int(mx)
    sum = int(0)

    print(f'Q: {q}')
    print(f'G: {g}')
    print(f'H: {h}')
    print(f'C: {c}')
    print(f'M: {m}')
    print(f'R: {r}')

    for i in r:
        sum = sum + int(i)
    return c == (pow(g, m, q) * pow(h, sum, q)) % q

print("[BOB]")
start()