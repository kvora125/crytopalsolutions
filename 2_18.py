def aes_128_ctr_keystream_block(key, nonce, block_count):
    return aes_128_ecb_enc(
        # '<Q' format is a little endian unsigned long long (64 bits)
        bytearray(pack('<Q', nonce)) + bytearray(pack('<Q', block_count)),
        key
    )

def aes_128_ctr_keystream_generator(key, nonce):
    block_count = 0
    while True:
        x = aes_128_ctr_keystream_block(bytes(key), nonce, block_count) 
        for byte in x:
            yield byte
        block_count += 1

def aes_128_ctr(buffer, key, nonce):
    def xor(b1, b2):
        b = bytearray()
        for byte in b1:
            # Note, we need to use b2.next() as it's a generator
            b.append(ord(byte) ^ b2.next())
        return b
    return xor(buffer, aes_128_ctr_keystream_generator(key, nonce))

# Don't forget to decode this string!
ciphertext = bytearray("L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==").decode("base64")
print aes_128_ctr(
    ciphertext,
    pad_pkcs7(bytearray("YELLOW SUBMARINE"), AES.block_size),
    0
)
# Yo, VIP Let's kick it Ice, Ice, baby Ice, Ice, baby
