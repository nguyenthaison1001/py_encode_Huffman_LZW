from struct import *


def encodeLZ(fileIn, fileOut):
    # defining the maximum table size
    # opening the input file
    # reading the input file and storing the file data into data variable
    maximum_table_size = pow(2, int(10))
    file = open(fileIn)
    data = file.read()

    # Building and initializing the dictionary.
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}
    # print(dictionary)
    string = ""                 # string to store the pad string
    comp_data = []              # variable to store the compressed data.

    # LZW Compression algorithm
    for symbol in data:
        string_symbol = string + symbol                 # get input symbol.
        if string_symbol in dictionary:
            string = string_symbol
        else:
            comp_data.append(dictionary[string])        # Add value of string into comp_data
            if len(dictionary) <= maximum_table_size:
                dictionary[string_symbol] = dict_size   # Add new string into dictionary
                dict_size += 1                          # and assign it value of dict_size
            string = symbol

    # Check the last string
    if string in dictionary:
        comp_data.append(dictionary[string])
        # print(comp_data)

    # Storing the compressed string into a file (byte-wise).
    output_file = open(fileOut, "wb")
    for data in comp_data:
        output_file.write(pack('>H', int(data)))

    # Closing all files
    output_file.close()
    file.close()

    print("Encoded successfully!")


def decodeLZ(fileIn, fileOut):
    file = open(fileIn, "rb")
    comp_data = []
    next_code = 256
    decomp_data = ""
    string = ""

    # Reading the compressed file.
    while True:
        rec = file.read(2)
        if len(rec) != 2:
            break
        (data,) = unpack('>H', rec)
        comp_data.append(data)

    # Building and initializing the dictionary.
    dict_size = 256
    dictionary = dict([(x, chr(x)) for x in range(dict_size)])

    # iterating through the codes.
    # LZW Decompression algorithm
    for code in comp_data:
        if not (code in dictionary):
            dictionary[code] = string + (string[0])
        decomp_data += dictionary[code]
        if not (len(string) == 0):
            dictionary[next_code] = string + (dictionary[code][0])
            next_code += 1
        string = dictionary[code]

    # Storing the decompressed string into a file.
    output_file = open(fileOut, "w")
    for data in decomp_data:
        output_file.write(data)

    # Closing all files
    output_file.close()
    file.close()

    print("Decoded successfully!")


# Running program
encodeLZ(fileIn="text1.txt", fileOut="text1_encode_LZW.bin")
decodeLZ(fileIn="text1_encode_LZW.bin", fileOut="text1_decode_LZW.txt")
