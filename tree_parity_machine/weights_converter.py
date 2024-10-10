import math
import numpy as np

class BinaryProcessor:
    def __init__(self, bits, L):
        self.bits = bits
        self.L = L
        self.first_bin = None
        self.next_new = None

    def bits_to_weights(self):
        """Convert a binary string into an array of weights."""
        if not self.bits:
            return np.array([])

        min_req_bits = math.ceil(math.log2(self.L + 1)) + 1
        # Split bits into chunks
        bits_list = [self.bits[i:i + min_req_bits] for i in range(0, len(self.bits), min_req_bits)]
        
        # Pad the last chunk if necessary
        bits_list[-1] = bits_list[-1].ljust(min_req_bits, '0')
        
        # Convert chunks to weights
        nums = [
            self._convert_chunk_to_weight(chunk) for chunk in bits_list
        ]

        # Handle out-of-range weights
        return self.handle_bits_outside_range(nums)

    def _convert_chunk_to_weight(self, chunk):
        """Convert a single chunk to its corresponding weight."""
        sign = 1 if chunk[0] == '0' else -1  # Determine sign from the first bit
        weight = int(chunk[1:], 2)  # Convert remaining bits to an integer
        return sign * weight

    def bits_to_arr(self, K, N):
        """Reshape the weight array to KxN dimensions."""
        weights = self.bits_to_weights()
        if len(weights) < K * N:
            raise ValueError("Not enough weights to reshape to the desired dimensions.")
        return np.reshape(weights, (K, N))

    def handle_bits_outside_range(self, nums):
        """Adjust weights that fall outside the specified range."""
        for i, element in enumerate(nums):
            if abs(element) > self.L:
                if self.first_bin is None:
                    self.first_bin = bin(abs(element))
                    self.next_new = int(self.first_bin[2:], 2)  # Skip '0b'
                else:
                    self.next_new = (self.next_new + 1) if self.next_new < self.L else -self.L
                nums[i] = self.next_new
        return nums

    def arr_to_bits(self, arr, length):
        """Convert a 2D array of weights back into a binary string."""
        number_list = arr.flatten().tolist()  # Flatten the array to 1D
        result_bits = [
            ("1" + bin(i)[3:] if i < 0 else "0" + bin(i)[2:]) for i in number_list
        ]

        # Pad binary strings to ensure uniform length
        max_len = max(len(bit) for bit in result_bits)
        padded_bits = [bit.zfill(max_len) for bit in result_bits]
        
        return ''.join(padded_bits)[:length]