# ALICE                               BOB
# NKL                         >       NKL
# a=create_TPM                >       b=create_TPM
# W = sha(a)
# W_b = Null
# while W != W_b:
#     UPDATE_W=True           >       UPDATE_W
#                                     While UPDATE_W:
#     X = nrand()             >           X
#     a_tau
#     B_tau                   <           b_tau
#                                         UPDATE_X = true
#     while a_tau!=b_tau                  while UPDATE_X:
#         X                   >               X
#         a_tau
#         b_tau               <               b_tau
#     UPDATE_X = False        >           UPDATE_X = false
#     a_update_W                          w=b_update_w
#     W_b                     <           sha(w)

import socket
import pickle
import numpy as np
import TPM

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

N = int(input("N: "))
K = int(input("K: "))
L = int(input("L: "))
machine_conf = [N, K, L]
W = np.random.randint(-L, L + 1, size=(K, N))
alice = TPM.Tpm(N, K, L, W)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    # with conn:
    data = pickle.dumps(machine_conf)
    conn.sendall(data)

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