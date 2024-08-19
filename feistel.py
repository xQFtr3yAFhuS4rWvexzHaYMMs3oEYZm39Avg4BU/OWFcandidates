import math

class Permutation:
    def __init__(self, binary_string, n):
        self.binary_string = binary_string
        self.n = n
        required_bits = math.ceil(math.log2(math.factorial(n)))
        if len(binary_string) < required_bits:
            raise ValueError(
                f"Error: The binary string is too short. Current length is {len(binary_string)}. It must be at least {required_bits} bits long to define a permutation of {n} items.")
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

def f_function(right_half, key):
    perm = Permutation(key, len(right_half))
    return ''.join(right_half[i] for i in perm.permutation), perm.permutation

def feistel_network(input_bits):
    split_index = len(input_bits) // 2
    left = input_bits[:split_index]
    right = input_bits[split_index:]
    states = [f"Initial Input: {input_bits}"]
    states.append(f"Initial State - Left: {left}, Right: {right}")

    for round_number in range(1, 5):
        if round_number == 4:
            base_key = right  # Use the right half in the last round
            key_side = "right"
        else:
            base_key = left  # Use the left half in the first three rounds
            key_side = "left"

        # Extend the key by concatenating it with itself until its length matches the length of the input
        while len(base_key) < len(input_bits):
            base_key += base_key[:len(input_bits) - len(base_key)]  # Append part of or full base_key to match the input length

        transformed, permutation = f_function(right, base_key)
        new_right = ''.join(str(int(a) ^ int(b)) for a, b in zip(left, transformed))
        left, right = new_right, left

        states.append(f"After Round {round_number} - Key derived from {key_side} - Left: {left}, Right: {right}, Permutation: {permutation}")

    final_output = left + right
    states.append(f"Final Output: {final_output}")
    return final_output, states

def test_bit_lengths():
    for bits in range(8, 17, 2):  # From 8 bits to 16 bits, incrementing by 2
        output_count = {}
        filename = f"feistel_{bits}bit_log.txt"

        with open(filename, "w") as log_file:
            log_file.write(f"Testing {bits}-bit lengths\n")
            for i in range(2 ** bits):
                binary_string = format(i, f'0{bits}b')
                output, states = feistel_network(binary_string)
                for state in states:
                    log_file.write(f"{state}\n")
                if output in output_count:
                    output_count[output] += 1
                else:
                    output_count[output] = 1

            # Adjusted collision count calculation:
            collision_count = sum(count - 1 for count in output_count.values() if count > 1)
            total_attempts = 2 ** bits
            collision_percentage = (collision_count / total_attempts) * 100
            log_file.write(f"Total collisions: {collision_count}\n")
            log_file.write(f"Collision Percentage: {collision_percentage:.2f}%\n")
            log_file.write("Collision Details:\n")
            for key, value in output_count.items():
                if value > 1:
                    log_file.write(f"Output {key}: Occurs {value} times\n")

            print(f"{bits}-bit processing complete. Collision Percentage: {collision_percentage:.2f}%")

test_bit_lengths()
