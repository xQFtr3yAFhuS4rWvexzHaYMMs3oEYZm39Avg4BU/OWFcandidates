import random
import math
import time
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


class Permutation:
    def __init__(self, binary_string, n):
        self.binary_string = binary_string
        self.n = n
        required_bits = math.ceil(math.log2(math.factorial(n)))
        if len(binary_string) < required_bits:
            raise ValueError(
                f"Error: The binary string is too short. It must be at least {required_bits} bits long to define a permutation of {n} items.")
        self.index = int(self.binary_string, 2) % math.factorial(n)
        self.permutation = self.calculate_permutation()

    def calculate_permutation(self):
        items = list(range(self.n))
        permutation = []
        temp_index = self.index
        while items:
            factorial = math.factorial(len(items) - 1)
            position = temp_index // factorial
            permutation.append(items.pop(position))
            temp_index %= factorial
        return permutation


def extend_key(key, required_length):
    while len(key) < required_length:
        key += key
    return key[:required_length]


def f_function(right_half, key):
    required_bits = math.ceil(math.log2(math.factorial(len(right_half))))
    extended_key = extend_key(key, required_bits)
    perm = Permutation(extended_key, len(right_half))
    permuted_half = ''.join(right_half[i] for i in perm.permutation)
    return permuted_half, perm.permutation


def feistel_network(input_bits):
    split_index = len(input_bits) // 2
    left = input_bits[:split_index]
    right = input_bits[split_index:]

    for round_number in range(1, 5):
        if round_number < 4:
            base_key = right
        else:
            base_key = left

        extended_key = extend_key(base_key, len(input_bits))
        transformed, permutation = f_function(right, extended_key)
        new_right = ''.join(str(int(a) ^ int(b)) for a, b in zip(left, transformed))
        left, right = right, new_right

    return left + right


def aes_encrypt(data, key):
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(padded_data) + encryptor.finalize()


def test_specific_bit_length(bits):
    input_bits = format(random.getrandbits(bits), f'0{bits}b')
    input_bytes = int(input_bits, 2).to_bytes(bits // 8, byteorder='big')

    aes_key = b'sixteen byte key'  # 16 bytes for AES

    print(f"Testing with {bits}-bit input: {input_bits}")

    # Timing Feistel Network Encryption
    start_time = time.time()
    feistel_output = feistel_network(input_bits)
    feistel_time = time.time() - start_time

    # Timing AES Encryption
    start_time = time.time()
    aes_output = aes_encrypt(input_bytes, aes_key)
    aes_time = time.time() - start_time

    print(f"Feistel Network output: {feistel_output}")
    print(f"Feistel Network Time: {feistel_time:.6f}s")
    print(f"AES output: {aes_output.hex()}")
    print(f"AES Time: {aes_time:.6f}s")
    print(f"AES Configuration: 128-bit block size, ECB mode, Key Length: {len(aes_key) * 8} bits")
    print(
        f"Feistel Configuration: Permutation based on {math.ceil(math.log2(math.factorial(len(input_bits) // 2)))} bits required for permutation")


if __name__ == "__main__":
    test_specific_bit_length(128)  # Test for 128-bit input
