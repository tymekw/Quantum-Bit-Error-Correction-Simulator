import pickle
import socket
import TPM
import bits


class BobClient:
    def __init__(self):
        self.s = None
        self.N = None
        self.L = None
        self.K = None
        self.W_bob = None
        self.bobTPM = None
        self.X = None
        self.seed = None
        self.HOST = '127.0.0.1'
        self.PORT = 65432
        self.bits = None
        self.bits_length = None
        self.num_of_synchro = 150

    def bind(self):
        print("BIIIIIIIIIIIIIND")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST, self.PORT))

    def receive_machine_config(self):
        data = self.s.recv(1024)
        self.N, self.K, self.L, self.seed, self.bits_length, self.num_of_synchro = pickle.loads(data)
        self.bits = bits.Bits(self.L)
        self.s.sendall(pickle.dumps("OK"))

    def generate_bits(self):
        self.bits.generate_bits(self.seed, self.bits_length)

    def create_random_bits(self):
        self.bits.generate_bits(self.seed, self.bits_length)
        self.bits.create_BER()

    def create_machine(self):
        self.W_bob = self.bits.bits_to_arr(self.K, self.N)
        self.bobTPM = TPM.Tpm(self.N, self.K, self.L, self.W_bob)

    def run_TPM_machine(self):
        print(self.W_bob)
        print(self.bobTPM.W)
        for i in range(0, self.num_of_synchro):

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
                self.bobTPM.calculate_tau(self.X)
                print("tau")
                data = pickle.dumps(self.bobTPM.tau)
                self.s.sendall(data)
                print("tau send")
                data = self.s.recv(10000000)
                common_X = pickle.loads(data)
                print(common_X)

            print(i)
            self.W_bob = self.bobTPM.update_weights(self.X)

        #ToDo check if weights are the same
        data = pickle.dumps(self.bobTPM.W)
        self.s.sendall(data)

        print("done")
        self.bits.bits = self.bits.arr_to_bits(self.bobTPM.W, self.bits_length)
