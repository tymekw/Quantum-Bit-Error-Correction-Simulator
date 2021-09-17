import math
import random
import numpy as np


def generate_bits(seed, length):
    random.seed(seed)
    b = random.getrandbits(length)
    b = b
    b = bin(b)
    b = b[2:]
    if len(b) != length:
        b = '0' * (length - len(b)) + b
    return b


def bits_to_arr(bits, L, K, N):
    max_val = L*2
    min_req_bits = math.ceil(math.log2(max_val+1))
    print(min_req_bits)
    bits_list = [bits[i:i + min_req_bits] for i in range(0, len(bits), min_req_bits)]
    print(bits_list)
    nums = [int("0b" + str(bit), 2) - max_val // 2 for bit in bits_list]
    print(nums)
    nums = nums[:N * K]
    # print(L)
    # print(nums)
    first_bin = None
    next_new = None
    for i, element in enumerate(nums):
        if element > L:
            if not first_bin:
                first_bin = bin(element + max_val//2)
                next_new = int('0b' + first_bin[3:], 2)
            else:
                if next_new < max_val:
                    next_new = next_new + 1
                else:
                    next_new = 0
            element = next_new - max_val //2
            nums[i] = element

    print(nums)
    arr = np.array(nums)
    return np.reshape(arr, (K, N))


bits = generate_bits("seed", 256)
print("bits: {}".format(bits))
print("bits length: {}".format(len(bits)))
bits_to_arr(bits,1,2,1,1)