import math
import numpy as np

def bits_to_arr(bits: str, L:int, K: int, N: int) -> np.array:
    """Reshape the weight array to KxN dimensions."""
    weights = bits_to_weights(bits, L)
    if len(weights) < K * N:
        raise ValueError("Not enough weights to reshape to the desired dimensions.")
    return np.reshape(weights, (K, N))

def bits_to_weights(bits: str, L: int) -> list[int]:
    """Convert a binary string into an array of weights."""
    if not bits:
        return np.array([])

    min_req_bits = math.ceil(math.log2(L + 1)) + 1
    # Split bits into chunks
    bits_list = [bits[i:i + min_req_bits] for i in range(0, len(bits), min_req_bits)]
    
    # Pad the last chunk if necessary
    bits_list[-1] = bits_list[-1].ljust(min_req_bits, '0')
    
    # Convert chunks to weights
    nums = [
        _convert_chunk_to_weight(chunk) for chunk in bits_list
    ]

    # Handle out-of-range weights
    return handle_bits_outside_range(nums)

def _convert_chunk_to_weight(chunk: list[str]) -> list[int]:
    """Convert a single chunk to its corresponding weight."""
    sign = 1 if chunk[0] == '0' else -1  # Determine sign from the first bit
    weight = int(chunk[1:], 2)  # Convert remaining bits to an integer
    return sign * weight

def handle_bits_outside_range(nums, L):
    """Adjust weights that fall outside the specified range."""
    for i, element in enumerate(nums):
        if abs(element) > L:
            if first_bin is None:
                first_bin = bin(abs(element))
                next_new = int(first_bin[2:], 2)  # Skip '0b'
            else:
                next_new = (next_new + 1) if next_new < L else -L
            nums[i] = next_new
    return nums

def arr_to_bits(arr: np.array, length: int) -> str:
    """Convert a 2D array of weights back into a binary string."""
    number_list = arr.flatten().tolist()  # Flatten the array to 1D
    result_bits = [
        ("1" + bin(i)[3:] if i < 0 else "0" + bin(i)[2:]) for i in number_list
    ]

    # Pad binary strings to ensure uniform length
    max_len = max(len(bit) for bit in result_bits)
    padded_bits = [bit.zfill(max_len) for bit in result_bits]
    
    return ''.join(padded_bits)[:length]

def _get_factors(n: int) -> list[int]:
    """Return a list of factors of n."""
    return [i for i in range(1, n + 1) if n % i == 0]

def get_possible_hidden_layer_size(number_of_weights: int) -> list[tuple[int, int]]:
    factors = _get_factors(number_of_weights)
    
    shapes = []
    for i in range(len(factors)):
        for j in range(i, len(factors)):
            if factors[i] * factors[j] == number_of_weights:
                shapes.append((factors[i], factors[j]))
    return shapes