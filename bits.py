import random
import numpy as np

class Bits:
    def __init__(self, L):
        self.bits = None
        self.BER = None
        self.type = 'random'
        self.L = L
        self.max_val = 2*self.L+1 + self.L//2
        self.s = len(bin(self.max_val))-2
        # needed_bits_len = len(bin(2*self.L))
        # self.max_val = int('0b' + str('1'*needed_bits_len))
        # self.s = len

    def change_L(self, L):
        self.L = L
        self.max_val = 2 * self.L + 1 + self.L // 2
        self.s = len(bin(self.max_val)) - 2

    def generate_bits(self, seed, length):
        random.seed(seed)
        b = random.getrandbits(length)
        b = bin(b)
        b = b[2:]
        self.bits = b

    def create_BER(self):
        b_list = [i for i in self.bits]
        if self.type == 'random':
            for _ in range(int(len(b_list) * 0.01*self.BER)):
                if b_list[random.randint(0, len(b_list) - 1)] == "1":
                    b_list[random.randint(0, len(b_list) - 1)] = "0"
                else:
                    b_list[random.randint(0, len(b_list) - 1)] = "1"

        elif self.type == 'block':
            start_idx = random.randint(0, len(b_list)*(1-self.BER) - 1)
            for i in range(int(len(b_list) * 0.01*self.BER)):
                if b_list[start_idx+i] == "1":
                    b_list[start_idx + i] = "0"
                else:
                    b_list[start_idx + i] = "1"

        self.bits = "".join(b_list)


    def bits_to_arr(self, K, N):
        bits_list = [self.bits[i:i + self.s] for i in range(0, len(self.bits), self.s)]
        nums = [int("0b" + str(bit), 2) - self.max_val // 2 for bit in bits_list]
        nums = nums[:N * K]
        print(self.L)
        print(nums)
        for i, element in enumerate(nums):

            if element > self.L:
                nums[i] = self.L
            elif element < -self.L:
                nums[i] = -self.L

        arr = np.array(nums)
        return np.reshape(arr, (K, N))


    def arr_to_bits(self, arr, max_val):
        al = []
        for row in arr:
            for el in row:
                al.append(el + max_val // 2)

        print(al)

        result_bits = [bin(int(i))[2:] for i in al]
        print(result_bits)
        max_len = len(max(result_bits, key=len))
        b = ['0' * (max_len - len(bit)) + bit for bit in result_bits]
        b = ''.join(b)
        return b
