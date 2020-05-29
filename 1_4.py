max_score = None
english_plaintext = None
key = None

# The ciphertexts are provided in a file named 4.txt
for line in open("4.txt", "r"):
    line = line.rstrip()
    b1 = bytearray.fromhex(line)

    for i in range(256):
        b2 = [i] * len(b1)
        plaintext = bytes(xor(b1, b2))
        pscore = score(plaintext)

        if pscore > max_score or not max_score:
            max_score = pscore
            english_plaintext = plaintext
            key = chr(i)

print key, english_plaintext
# 5 Now that the party is jumping
