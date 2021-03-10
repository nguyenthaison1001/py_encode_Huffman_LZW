from huffman3 import HuffmanCoding
import sys

fileIn = "text1.txt"
fileOut = "text1_decoding.txt"

h = HuffmanCoding(fileIn, fileOut)

output_path = h.encodeHuffman()
print("Encoding file : " + output_path)

decom_path = h.decodeHuffman(output_path)
print("Decoding file : " + decom_path)
