def hamming_distance(enc_str1, enc_str2):
    differing_bits = 0
    for byte in xor(b1, b2):
        differing_bits += bin(byte).count("1")
    return differing_bits

b1 = bytearray("this is a test")
b2 = bytearray("wokka wokka!!!")

hamming_distance(b1, b2)
# 37
