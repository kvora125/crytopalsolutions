def crack_keystream(ciphertexts):
    keystream = bytearray()
    max_ciphertext_length = max(map(len, ciphertexts))
    for i in range(max_ciphertext_length):
        bytes_at_index = map(
            ord, # Convert bytes to ints for XOR'ing
            filter(
                lambda x: x, # Filter out empty bytes
                map(
                    lambda x: x[i:i + 1], # Try to get the byte at i index
                    ciphertexts
                )
            )
        )
        max_score = None
        key = None
        for guess in range(256):
            b2 = [guess] * len(bytes_at_index)
            decrypted_bytes = bytes(xor(bytes_at_index, b2))
            pscore = score(decrypted_bytes)
            if pscore > max_score or not max_score:
                max_score = pscore
                key = chr(guess)
        keystream.append(key)
    return keystream

key = random_key(AES.block_size)
FIXED_NONCE = 0
ciphertexts = []
for encoded_plaintext in list(open("19.txt", "r")):
    plaintext = bytearray(encoded_plaintext).decode("base64")
    ciphertexts.append(aes_128_ctr(plaintext, key, FIXED_NONCE))

keystream = crack_keystream(ciphertexts)
for ciphertext in ciphertexts:
    print xor(ciphertext, keystream)
