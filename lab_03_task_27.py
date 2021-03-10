from lab_03_11_Huffman import HuffmanCoding
from lab_03_11_LZW import encodeLZ, decodeLZ

# Compress Huffman
def method_Huffman():
    print("\nMethod Huffman:")
    fileIn = "text_02.txt"
    fileOut = "text_02_decode_huffman.txt"

    h = HuffmanCoding(fileIn, fileOut)

    output_path = h.encodeHuffman()
    print("Encoded path:" + output_path)

# Compress LZW
def method_LZW():
    print("\nMethod LZW:")
    encodeLZ(fileIn="text_02.txt", fileOut="text_02_encode_LZW.bin")

# Running encode
method_Huffman()
method_LZW()

# Informations of sizes (unit: bytes)
size_text02_uncompressed = 2.559

size_text02_huffman_compressed = 1.397
size_text02_LZW_compressed = 2.354

# Data compression ratio
Huffman = size_text02_huffman_compressed/size_text02_huffman_compressed

ratHuff = float(size_text02_huffman_compressed/size_text02_huffman_compressed)
ratLZW = float(size_text02_huffman_compressed/size_text02_LZW_compressed)

print("\nResult:")
print("Data compression ratio of method Huffman: ", ratHuff)
print("Data compression ratio of method LZW: ", ratLZW)

# Compare 2 compression ratios
print("\nComments:")
if ratHuff > ratHuff:
    print("Method Huffman is more optimal than LZW.")
else:
    print("Method LZW is more optimal than Huffman.")

# Similar to text 03
print("\nRealizing the same with text 03")
