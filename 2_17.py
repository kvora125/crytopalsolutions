input_strings = [
    "MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
    "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
    "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
    "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
    "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
    "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
    "MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
    "MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
    "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
    "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93",
]

rand_key = None

# Slight modification of the previously defined aes_128_cbc_dec function.
# We don't unpad the decrypted ciphertext in this method.
def aes_128_cbc_dec(ciphertext, key, iv):
    plaintext = bytearray(len(ciphertext))
    prev_block = iv
    for i in range(0, len(ciphertext), AES.block_size):
        plaintext[i: i + AES.block_size] = xor(
            aes_128_ecb_dec(bytes(ciphertext[i: i + AES.block_size]), key),
            prev_block
        )
        prev_block = ciphertext[i: i + AES.block_size]
    return plaintext

def cbc_enc_random_string(input_strings):
    global rand_key
    rand_key = random_key(AES.block_size)
    input_string = input_strings[randint(0, len(input_strings) - 1)]
    iv = random_key(AES.block_size)
    return aes_128_cbc_enc(input_string, bytes(rand_key), iv), iv

def padding_oracle(ciphertext, iv):
    input_string = aes_128_cbc_dec(ciphertext, bytes(rand_key), iv)
    try:
        unpad_valid_pkcs7(input_string)
        return True
    except:
        return False
def crack_block(block, iv):
    plaintext_block = bytearray()
    start_guess = 0
    while len(plaintext_block) < AES.block_size:
        for guess in range(start_guess, 256):
            padding = len(plaintext_block) + 1
            # Copy the IV so we don't corrupt it for future guesses
            corrupted_iv = bytearray(iv)
            for byte in range(1, padding + 1):
                # Use the "correct" guesses of plaintext block bytes
                if byte < padding:
                    corrupted_iv[-byte] =  bytes(xor(
                        xor(
                            bytearray([iv[-byte]]),
                            bytearray(chr(plaintext_block[-byte]))
                        ),
                        bytearray(chr(padding))
                    ))
                # Guess the correct byte
                else:
                    corrupted_iv[-byte] =  bytes(xor(
                        xor(bytearray([iv[-byte]]), bytearray(chr(guess))),
                        bytearray(chr(padding))
                    ))
            if padding_oracle(block, corrupted_iv):
                # If the padding oracle doesn't complain... we've guessed the
                # correct byte!
                plaintext_block = bytearray(chr(guess)) + plaintext_block
                start_guess = 0
                break
        else:
            # If we cannot find a correct padding, the guess for the previous
            # byte was incorrect... so try another one!
            try:
                start_guess = int(plaintext_block[0]) + 1
                plaintext_block = plaintext_block[1:]
            except:
                # This occurs if the last ciphertext block is just a padding
                # block... I don't know why my encryption is sometimes adding
                # an extra block
                return bytearray()
    return plaintext_block

def crack(ciphertext, iv):
    ciphertext = iv + ciphertext
    plaintext = ''
    for i in range(len(ciphertext) / AES.block_size):
        # We only really need to pass two blocks to the padding oracle...
        # The block to the decrypt, and the one before it which we corrupt
        plaintext += crack_block(
            ciphertext[(i + 1) * AES.block_size: (i + 2) * AES.block_size],
            ciphertext[i * AES.block_size: (i + 1) * AES.block_size]
        )
    return unpad_valid_pkcs7(plaintext)

ciphertext, iv = cbc_enc_random_string(input_strings)
plaintext = crack(ciphertext, iv)
print plaintext
