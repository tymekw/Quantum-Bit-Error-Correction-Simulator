import socket
import pickle
import subprocess

import numpy as np
import TPM


# N = int(input("N: "))
# K = int(input("K: "))
# L = int(input("L: "))
def run(N, K, L):

    HOST = '127.0.0.1'
    PORT = 65432

    print("runs")
    machine_conf = [N, K, L]
    W = np.random.randint(-L, L + 1, size=(K, N))
    alice = TPM.Tpm(N, K, L, W)
    print("goes")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("before bind")
        subprocess.Popen("start /wait python bob_client.py", shell=True)
        s.bind((HOST, PORT))
        print("bind")

        s.listen()
        conn, addr = s.accept()
        # with conn:
        data = pickle.dumps(machine_conf)
        conn.sendall(data)
        print("waits")
        for i in range(0, 150):

            print("inside loop")
            bob_tau = None
            alice.tau = 1
            while alice.tau != bob_tau:
                print("choose X")
                try:
                    s.listen()
                    conn, addr = s.accept()
                except:
                    print("still ok")
                X = np.random.randint(-L, L + 1, size=(K, N))
                alice.calculate_tau(X)
                print("sending X")
                data = pickle.dumps(X)
                conn.sendall(data)
                print("X send")
                rec_tau = conn.recv(1000000)
                bob_tau = pickle.loads(rec_tau)

                if alice.tau == bob_tau:
                    data = pickle.dumps(1)
                    conn.sendall(data)
                    print("X chosen")
                else:
                    data = pickle.dumps(0)
                    conn.sendall(data)
                    print("X not chosen")
            print(i)
            alice.update_weights(X)

        print("outside loop")
        bob_w = conn.recv(1000000)
        bob_wei = pickle.loads(bob_w)
        if np.array_equal(alice.W, bob_wei):
            print('dziala')

        print("done")

    print(alice.W)
