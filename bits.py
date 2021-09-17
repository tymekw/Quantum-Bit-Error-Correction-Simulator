import random
import numpy as np
import math

class Bits:
    def __init__(self, L):
        self.bits = None
        self.BER = None
        self.type = 'random'
        self.L = L
        self.max_val = 2*self.L

    def change_L(self, L):
        self.L = L
        self.max_val = 2 * self.L + 1 + self.L // 2

    def generate_bits(self, seed, length):
        random.seed(seed)
        b = random.getrandbits(length)
        b = b
        b = bin(b)
        b = b[2:]
        if len(b) != length:
            b = '0' * (length - len(b)) + b
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
            how_many_to_change = int(len(b_list) * 0.01*self.BER)
            start_idx = random.randint(0, len(b_list)- 1 - how_many_to_change)
            for i in range(how_many_to_change):
                if b_list[start_idx+i] == "1":
                    b_list[start_idx + i] = "0"
                else:
                    b_list[start_idx + i] = "1"

        self.bits = "".join(b_list)

    def bits_to_arr(self, K, N):
        min_req_bits = math.ceil(math.log2(self.max_val + 1))
        bits_list = [self.bits[i:i + min_req_bits] for i in range(0, len(self.bits), min_req_bits)]
        if len(bits_list[-1]) < min_req_bits:
            bits_list[-1] = '0'*( min_req_bits - len(bits_list[-1]))  +bits_list[-1]
        nums = [int("0b" + str(bit), 2) - self.max_val // 2 for bit in bits_list]
        nums = nums[:N * K]
        self.first_bin = None
        self.next_new = None
        nums = self.handle_bits_outside_range(nums)
        arr = np.array(nums)
        return np.reshape(arr, (K, N))

    def handle_bits_outside_range(self, nums):
        for i, element in enumerate(nums):
            if element > self.L:
                if not self.first_bin:
                    self.first_bin = bin(element + self.max_val // 2)
                    self.next_new = int('0b' + self.first_bin[3:], 2)
                else:
                    if self.next_new < self.max_val:
                        self.next_new = self.next_new + 1
                    else:
                        self.next_new = 0
                element = self.next_new - self.max_val // 2
                nums[i] = element
        return nums

    def arr_to_bits(self, arr, length):
        al = []
        for row in arr:
            for el in row:
                al.append(el + self.max_val // 2)
        result_bits = [bin(int(i))[2:] for i in al]
        max_len = len(max(result_bits, key=len))
        b = ['0' * (max_len - len(bit)) + bit for bit in result_bits]
        b = ''.join(b)
        return b[:length]
