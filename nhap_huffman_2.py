from Huffman import HuffmanCoding

#input file path
path = "D:/Nguyen Thai Son/Freshman/Infor/lab 6/Lab_06/text1.txt"
# D:/Nguyen Thai Son/Freshman/Infor/lab 6/Lab_06/text1.txt
h = HuffmanCoding(path)
output_path = h.compress()
h.decompress(output_path)