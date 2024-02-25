import secrets
import functools

def generate_256_bit_string(bitsize):
    return ''.join(secrets.choice('01') for _ in range(bitsize))

def split_string_into_boxes(bit_string, box_size=32):
    return [bit_string[i:i+box_size] for i in range(0, len(bit_string), box_size)]

def xor_chunks(chunk_a, chunk_b):
    return ''.join('1' if bit_a != bit_b else '0' for bit_a, bit_b in zip(chunk_a, chunk_b))

def generate_permutation_from_z(z_string, permutation_size=32):
    chunk_size = len(z_string) // permutation_size
    indices = [int(z_string[i:i+chunk_size], 2) % permutation_size for i in range(0, len(z_string), chunk_size)]
    return sorted(range(permutation_size), key=indices.__getitem__)

def apply_permutation(box, permutation):
    return ''.join(box[i] for i in permutation)

def xor_all_elements(elements):
    return functools.reduce(xor_chunks, elements)

def blackbox(input_string):
    boxes = split_string_into_boxes(input_string)
    chunks_after_permutation = [
        apply_permutation(box, generate_permutation_from_z(
            xor_chunks(''.join(boxes[:i] + boxes[i+1:])[:105], ''.join(boxes[:i] + boxes[i+1:])[105:210]) +
            ''.join(boxes[:i] + boxes[i+1:])[210:]
        )) for i, box in enumerate(boxes)
    ]

    return ''.join(xor_all_elements(chunks_after_permutation[i:i+3]) for i in range(len(chunks_after_permutation)))

class MerkleTree:
    def __init__(self, input_string):
        self.input_string = input_string
        self.leaf_nodes = self.generate_leaf_nodes()
        self.root = self.build_tree()

    def generate_leaf_nodes(self):
        chunk_size = 256
        return [self.input_string[i:i+chunk_size] for i in range(0, len(self.input_string), chunk_size)]

    def commitment_function(self, input_string):
        return blackbox(input_string)

    def build_tree(self):
        tree = [self.leaf_nodes]
        while len(tree[-1]) > 1:
            tree.append([
                ''.join('1' if bit1 != bit2 else '0' for bit1, bit2 in zip(
                    self.commitment_function(node1),
                    self.commitment_function(node2[::-1]) if node2 else self.commitment_function(node1)
                )) for node1, node2 in zip(tree[-1][::2], tree[-1][1::2] + [""])
            ])
        return tree[-1][0]

if __name__ == "__main__":
    secure_input_string = generate_256_bit_string(1024)
    merkle_tree = MerkleTree(secure_input_string)
    print(merkle_tree.root)
