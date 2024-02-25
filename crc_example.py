from sage.all import *
import libscrc
import numpy as np
import pandas as pd

BINARY_LENGTH = 4
CRC_MODE = 4
MATRIX_SIZE = 8

class StringCheckSum:
    def __init__(self, first_input_str, second_input_str, crc_length):
        self.first_input_bin = first_input_str
        self.second_input_bin = second_input_str
        self.crc_length = crc_length
        self.first_input_bytes = self._bitstring_to_bytes(self.first_input_bin)
        self.second_input_bytes = self._bitstring_to_bytes(self.second_input_bin)
        self.first_crc = self._calculate_crc(self.first_input_bytes, crc_length)
        self.second_crc = self._calculate_crc(self.second_input_bytes, crc_length)
        self.first_crc_bin = bin(self.first_crc)[2:].zfill(BINARY_LENGTH)
        self.second_crc_bin = bin(self.second_crc)[2:].zfill(BINARY_LENGTH)
        self.first_crc_bin_perm, self.second_crc_bin_perm = self._permute_bits_of_crc(self.first_crc_bin, self.second_crc_bin)
        self.first_input_with_crc_bin = self.first_input_bin + self.first_crc_bin_perm
        self.second_input_with_crc_bin = self.second_crc_bin_perm + self.second_input_bin
        self.xor_with_crc_bin = bin(int(self.first_input_with_crc_bin, 2) ^ int(self.second_input_with_crc_bin, 2))[2:].zfill(BINARY_LENGTH + CRC_MODE)

    @staticmethod
    def _bitstring_to_bytes(s):
        return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

    @staticmethod
    def _calculate_crc(input_bytes, crc_length):
        if crc_length == 4:
            return libscrc.itu4(input_bytes)

    @staticmethod
    def _permute_bits_of_crc(crc1, crc2):
        combined = crc1 + crc2
        p, q = combined[:3], combined[3:6]
        p_dec, q_dec = int(p, 2), int(q, 2)
        swapped = list(crc2 + crc1)
        swapped[p_dec], swapped[q_dec] = swapped[q_dec], swapped[p_dec]
        return ''.join(swapped[:4]), ''.join(swapped[4:])

def generate_binary_strings(bit_count):
    return [format(i, f'0{bit_count}b') for i in range(2 ** bit_count)]

def generate_diagonal_matrix(size):
    return diagonal_matrix(ZZ, [1]*size)

def generate_matrix_A(checksum_objects):
    A_matrix = []
    for checksum in checksum_objects:
        xor_result = int(checksum.xor_with_crc_bin, 2)
        row = [int(bit) for bit in format(xor_result, f'0{MATRIX_SIZE}b')]
        A_matrix.append(row)
    return matrix(GF(2), A_matrix)

def main():
    s1_set = generate_binary_strings(BINARY_LENGTH)
    s2_set = generate_binary_strings(BINARY_LENGTH)
    checksum_objects = [StringCheckSum(s1, s2, CRC_MODE) for s1 in s1_set for s2 in s2_set]
    
    diagonal_matrix = generate_diagonal_matrix(MATRIX_SIZE)
    A_matrix = generate_matrix_A(checksum_objects)

    # Example of matrix usage
    print("Diagonal Matrix:")
    print(diagonal_matrix)
    print("A Matrix based on CRC calculations and permutations:")
    print(A_matrix)

if __name__ == '__main__':
    main()
