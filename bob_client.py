import pickle
import socket
import numpy as np
import TPM
import bits


class BobClient:
    def __init__(self):
        self.s = None
        self.N = None
        self.L = None
        self.K = None
        self.W_bob = None
        self.bob = None
        self.X = None
        self.seed = None
        self.HOST = '127.0.0.1'
        self.PORT = 65432
        self.bits = bits.Bits(2)
        self.bits_length = None

    def bind(self):
        print("BIIIIIIIIIIIIIND")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST, self.PORT))

    def receive_machine_config(self):
        data = self.s.recv(1024)
        self.N, self.K, self.L, self.seed, self.bits_length = pickle.loads(data)
        self.s.sendall(pickle.dumps("OK"))

    def create_random_bits(self):
        self.bits.generate_bits(self.seed, self.bits_length)
        self.bits.create_BER(3, 'random')
        self.W_bob = self.bits.bits_to_arr(self.K, self.N)
        print(self.W_bob)

    def create_machine(self):
        self.bob = TPM.Tpm(self.N, self.K, self.L, self.W_bob)

    def run_TPM_machine(self):
        for i in range(0, 150):

            print("inside loop")
            common_X = False
            while not common_X:
                print("choose X")
                try:
                    self.s.close()
                    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.s.connect((self.HOST, self.PORT))
                except socket.error:
                    print("socket error")
                x = self.s.recv(1000000)
                print("x reciv")
                self.X = pickle.loads(x)
                self.bob.calculate_tau(self.X)
                print("tau")
                data = pickle.dumps(self.bob.tau)
                self.s.sendall(data)
                print("tau send")
                data = self.s.recv(10000000)
                common_X = pickle.loads(data)
                print(common_X)

            print(i)
            self.bob.update_weights(self.X)

        data = pickle.dumps(self.bob.W)
        self.s.sendall(data)

        print(self.bob.W)
        print("done")
