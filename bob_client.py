import pickle
import socket
import numpy as np
import TPM

# def run():
HOST = '127.0.0.1'
PORT = 65432



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
# s.sendall(b'Hello, world')

data = s.recv(1024)
N, K, L = pickle.loads(data)

W_bob = np.random.randint(-L, L + 1, size=(K, N))
bob = TPM.Tpm(N, K, L, W_bob)

for i in range(0, 150):

    print("inside loop")
    common_X = False
    while not common_X:
        print("choose X")
        try:
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
        except socket.error:
            print("still works")
        x = s.recv(1000000)
        print("x reciv")
        X = pickle.loads(x)
        bob.calculate_tau(X)
        print("tau")
        # with s:
        data = pickle.dumps(bob.tau)
        s.sendall(data)
        print("tau send")
        data = s.recv(10000000)
        common_X = pickle.loads(data)
        print(common_X)

    print(i)
    bob.update_weights(X)

data = pickle.dumps(bob.W)
s.sendall(data)

print(bob.W)
print("done")
