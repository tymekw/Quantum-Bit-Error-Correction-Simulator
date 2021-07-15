import socket
import pickle
import bits
import numpy as np
import TPM


class AliceServer:
    def __init__(self):
        self.N = 10
        self.K = 5
        self.L = 5
        self.HOST = '127.0.0.1'
        self.PORT = 65432
        self.s = None
        self.conn = None
        self.addr = None
        self.machine_conf = None
        self.W = None
        self.alice = None
        self.X = None
        self.bits = bits.Bits(2)
        self.seed = 10

    def bind(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("before bind")
        self.s.bind((self.HOST, self.PORT))
        print("bind")

        self.s.listen()
        self.conn, self.addr = self.s.accept()

    def create_machine(self):
        self.machine_conf = [self.N, self.K, self.L, self.seed]
        self.bits.generate_bits(self.seed, 1000)
        self.W = self.bits.bits_to_arr(self.K, self.N)
        print(self.W)
        self.alice = TPM.Tpm(self.N, self.K, self.L, self.W)

    def send_machine_config(self):
        data = pickle.dumps(self.machine_conf)
        self.conn.sendall(data)

    def run_machine(self):

        print("waits")
        for i in range(0, 1500):
            print("inside loop")
            bob_tau = None
            self.alice.tau = 1
            while self.alice.tau != bob_tau:
                print("choose X")
                try:
                    self.s.listen()
                    self.conn, self.addr = self.s.accept()
                except:
                    print("socket error")

                self.X = np.random.randint(-self.L, self.L + 1, size=(self.K, self.N))
                self.alice.calculate_tau(self.X)
                print("sending X")
                data = pickle.dumps(self.X)
                self.conn.sendall(data)
                print("X send")
                rec_tau = self.conn.recv(1000000)
                bob_tau = pickle.loads(rec_tau)

                if self.alice.tau == bob_tau:
                    data = pickle.dumps(1)
                    self.conn.sendall(data)
                    print("X chosen")
                else:
                    data = pickle.dumps(0)
                    self.conn.sendall(data)
                    print("X not chosen")
            print(i)
            self.alice.update_weights(self.X)

        print("outside loop")
        bob_w = self.conn.recv(1000000)
        bob_wei = pickle.loads(bob_w)
        if np.array_equal(self.alice.W, bob_wei):
            print('dziala')

        print("done")

        print(self.alice.W)


    # def start(self):
    #     HOST = '127.0.0.1'
    #     PORT = 65432
    #
    #     print("runs")
    #     machine_conf = [self.n, self.k, self.l]
    #     W = np.random.randint(-self.l, self.l + 1, size=(self.k, self.n))
    #     alice = TPM.Tpm(self.n, self.k, self.l, W)
    #     print("goes")
    #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.s:
    #         print("before bind")
    #         # subprocess.Popen("start /wait python bob_client.py", shell=True)
    #         self.s.bind((HOST, PORT))
    #         print("bind")
    #
    #         self.s.listen()
    #         conn, addr = self.s.accept()
    #         # with conn:
    #         data = pickle.dumps(machine_conf)
    #         conn.sendall(data)
    #         print("waits")
    #         for i in range(0, 1500):
    #             self.num = i
    #             print("inside loop")
    #             bob_tau = None
    #             alice.tau = 1
    #             while alice.tau != bob_tau:
    #                 print("choose X")
    #                 try:
    #                     self.s.listen()
    #                     conn, addr = self.s.accept()
    #                 except:
    #                     print("still ok")
    #                 self.X = np.random.randint(-self.l, self.l + 1, size=(self.k, self.n))
    #                 alice.calculate_tau(self.X)
    #                 print("sending X")
    #                 data = pickle.dumps(self.X)
    #                 self.conn.sendall(data)
    #                 print("X send")
    #                 rec_tau = self.conn.recv(1000000)
    #                 bob_tau = pickle.loads(rec_tau)
    #
    #                 if alice.tau == bob_tau:
    #                     data = pickle.dumps(1)
    #                     conn.sendall(data)
    #                     print("X chosen")
    #                 else:
    #                     data = pickle.dumps(0)
    #                     conn.sendall(data)
    #                     print("X not chosen")
    #             print(i)
    #             alice.update_weights(X)
    #
    #         print("outside loop")
    #         bob_w = conn.recv(1000000)
    #         bob_wei = pickle.loads(bob_w)
    #         if np.array_equal(alice.W, bob_wei):
    #             print('dziala')
    #
    #         print("done")
    #
    #     print(alice.W)
