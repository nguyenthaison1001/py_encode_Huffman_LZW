import heapq
import os


class HuffmanCoding:
    def __init__(self, fileIn, fileOut):
        self.fileIn = fileIn
        self.fileOut = fileOut
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}  # Used to convert dict to decode

    class HeapNode:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        # defining comparators less_than and equals
        def __lt__(self, other):
            return self.freq < other.freq

    """ functions for compression: """

    def make_frequency_dict(self, text):  # Calculate frequencies and save as a dict
        frequency = {}
        for character in text:
            if character not in frequency:
                frequency[character] = 0
            frequency[character] += 1
        return frequency

    def make_heap(self, frequency):  # Assign char and freq from dict to heapNode
        for key in frequency:
            node = self.HeapNode(key, frequency[key])  # init new node
            heapq.heappush(self.heap, node)  # insert new node and sort

    def merge_nodes(self):  # Build binary tree
        while len(self.heap) > 1:  # node = 1 -> stop the loop
            node1 = heapq.heappop(self.heap)  # remove and return 2 smallest
            node2 = heapq.heappop(self.heap)  # elements from heap

            merged = self.HeapNode(None, node1.freq + node2.freq)  # merged 2 min elements
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)  # insert node 'merged', sort

    def make_codes_helper(self, root, current_code):
        if root is None:
            return

        # Save Huffman code into 2 dict. 1 is to encode, 1 to decode
        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    # Start make codes
    def make_codes(self):
        root = heapq.heappop(self.heap)  # Init root
        current_code = ""
        self.make_codes_helper(root, current_code)

    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8  # number of 0 to add
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    # Add 0 so that length is a multiple of 8
    def get_byte_array(self, padded_encoded_text):
        if len(padded_encoded_text) % 8 != 0:
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):    # loop with step = 8
            byte = padded_encoded_text[i:i + 8]            # get element from  i to (i+8)
            b.append(int(byte, 2))                         # base 2
        return b

    def encodeHuffman(self):
        filename, file_extension = os.path.splitext(self.fileIn)
        output_path = filename + "_encode_huffman" + ".bin"

        with open(self.fileIn, 'r+') as file, open(output_path, 'wb') as output:
            text = file.read()
            text = text.rstrip()

            frequency = self.make_frequency_dict(text)
            self.make_heap(frequency)
            self.merge_nodes()
            self.make_codes()

            encoded_text = self.get_encoded_text(text)
            padded_encoded_text = self.pad_encoded_text(encoded_text)

            b = self.get_byte_array(padded_encoded_text)
            output.write(bytes(b))
        print("Encoded successfully!")
        return output_path

    """ functions for decompression: """

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]  # padded_info = 8 first bits
        extra_padding = int(padded_info, 2)  # 6

        padded_encoded_text = padded_encoded_text[8:]  # remove 8 first bits (infor)
        encoded_text = padded_encoded_text[:-1 * extra_padding]  # remove 6 last bits (extra)

        return encoded_text

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text

    def decodeHuffman(self, input_path):
        output_path = fileOut

        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            bit_string = ""

            byte = file.read(1)
            while len(byte) > 0:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

            encoded_text = self.remove_padding(bit_string)

            decompressed_text = self.decode_text(encoded_text)

            output.write(decompressed_text)

        print("Decoded successfully!")
        return output_path


# Running program
if __name__ == '__main__':
    fileIn = "text1.txt"
    fileOut = "text1_decode_huffman.txt"

    h = HuffmanCoding(fileIn, fileOut)

    output_path = h.encodeHuffman()
    print("Encoded path:" + output_path)

    decom_path = h.decodeHuffman(output_path)
    print("Decoded path:" + decom_path)
