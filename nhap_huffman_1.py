import ast
import heapq
import os


class HeapNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return other.freq > self.freq


class HuffmanCoding:
    def __init__(self, path):
        # self.fileIn = fileIn
        # self.fileOut = fileOut
        self.path = path
        self.heap = []                  # init static valuables
        self.codes = {}
        self.reverse_mapping = {}

    def make_frequency_dict(self, fileIn):
        frequency = dict()
        for line in fileIn:
            for character in line:
                if character not in frequency:
                    frequency[character] = 1
                else:
                    frequency[character] += 1
        return frequency  # da return ve kieu dictionary

    def make_heap(self, frequency):       # convert dict -> heap, contains char and freq
        for key in frequency:
            node = HeapNode(key, frequency[key])    # init new node
            heapq.heappush(self.heap, node)         # insert new node and sort

    def merge_nodes(self):  # build tree
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)    # remove and return 2 smallest
            node2 = heapq.heappop(self.heap)    # elements from heap

            # init a new heap of sum 2 min node
            # char of heap -> none, freq = freq1 + freq2
            merged = HeapNode(None, node1.freq + node2.freq)
            merged.left = node1             # tiep tuc re nhanh
            merged.right = node2

            heapq.heappush(self.heap, merged)     # insert node 'merged' -> into heap

    def make_codes_helper(self, root, current_code):    # root la 1 node
        if root is None:
            return

        if root.char is not None:
            self.codes[root.char] = current_code    # insert vao dict codes - curr_code
            self.reverse_mapping[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):       # tao code cho node root ban dau
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)

    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        if len(padded_encoded_text) % 8 != 0:
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8): # loop every 8 character
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

    def compress(self, filename):
        file_text = open(filename, 'r')
        lipsum = file_text.read()  # Read file
        lipsum = lipsum.rstrip()  # Return a copy of the string with trailing whitespace removed
        file_text.close()

        freq = self.make_frequency_dict(lipsum)
        self.make_heap(freq)
        self.merge_nodes()
        self.make_codes()

        encoded_text = self.get_encoded_text(lipsum)
        padded_encoded_text = self.pad_encoded_text(encoded_text)

        byte_array_huff = self.get_byte_array(padded_encoded_text)

        # write header
        filename_split = filename.split('.')
        js = open(filename_split[0] + "_compressed.bin", 'wb')  # filename_split[0] is filename
        strcode = str(self.codes)
        js.write(strcode.encode())
        js.close()

        # append new line for separation
        append = open(filename_split[0] + "_compressed.bin", 'a')
        append.write('\n')
        append.close()

        # append the rest of the "byte array"
        f = open(filename_split[0] + "_compressed.bin", 'ab')
        f.write(bytes(byte_array_huff))
        f.close()

        print('Compression Done!')


    """ functions for decompression: """

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1 * extra_padding]

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

    def decompress(self, compressedfile):
        filename_split = compressedfile.split('_')
        # get "header"
        header = open(compressedfile, 'rb').readline().decode()
        # header as object literal
        header = ast.literal_eval(header)
        # reverse mapping for better performance
        self.reverse_mapping = {v: k for k, v in header.items()}

        # get body
        f = open(compressedfile, 'rb')

        # get "body" as list.  [1:] because header
        body = f.readlines()[1:]
        f.close()

        bit_string = ""

        # merge list "body"
        # flattened the byte array
        join_body = [item for sub in body for item in sub]
        for i in join_body:
            bit_string += "{0:08b}".format(i)

        encoded_text = self.remove_padding(bit_string)

        # decompress start here
        current_code = ""
        decoded_text = ""
        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                decoded_text += self.reverse_mapping[current_code]
                current_code = ""

        # shameful code below, no reverse mapping.
        # for bit in encoded_text:
        #     current_code += bit
        #     if current_code in self.reverse_mapping.values():
        #         for key in self.reverse_mapping:
        #             if current_code == self.reverse_mapping[key]:
        #                 decoded_text += key
        #                 current_code = ""

        write = open(filename_split[0] + "_decompressed.txt", 'w')
        write.writelines(decoded_text)
        write.close()
        print('Decompression Done!')


if __name__ == '__main__':
    path = "text1.txt"
    h = HuffmanCoding(path)
    output_path = h.compress(path)
    path2 = "text1_compressed.bin"
    h.decompress(path2)
