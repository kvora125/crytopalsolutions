key = bytes(random_key(16))

def encryption_oracle(data):
    unknown_string = bytearray((
        "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\n" +
        "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\n" +
        "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\n" +
        "YnkK"
    ).decode("base64"))
    plaintext = pad_pkcs7(
        data + unknown_string,
        AES.block_size,
    )
    return aes_128_ecb_enc(plaintext, key)
 def get_block_size(oracle):
    ciphertext_length = len(oracle(bytearray()))
    i = 1
    while True:
        data = bytearray("A" * i)
        new_ciphertext_length = len(oracle(data))
        block_size = new_ciphertext_length - ciphertext_length
        if block_size:
            return block_size
        i += 1
def get_block_size(oracle):
    ciphertext_length = len(oracle(bytearray()))
    i = 1
    while True:
        data = bytearray("A" * i)
        new_ciphertext_length = len(oracle(data))
        block_size = new_ciphertext_length - ciphertext_length
        if block_size:
            return block_size
        i += 1
def get_unknown_string_size(oracle):
    ciphertext_length = len(oracle(bytearray()))
    i = 1
    while True:
        data = bytearray("A" * i)
        new_ciphertext_length = len(oracle(data))
        if ciphertext_length != new_ciphertext_length:
            return new_ciphertext_length - i
        i += 1
def get_unknown_string(oracle):
    block_size = get_block_size(oracle)
    is_ecb = is_ecb_mode(
        oracle(bytearray("YELLOW SUBMARINE" * 2)),
        block_size,
    )
    assert is_ecb
    unknown_string_size = get_unknown_string_size(oracle)

    unknown_string = bytearray()
    unknown_string_size_rounded = (
        ((unknown_string_size / block_size) + 1) *
        block_size
    )
    for i in range(unknown_string_size_rounded - 1, 0, -1):
        d1 = bytearray("A" * i)
        c1 = oracle(d1)[:unknown_string_size_rounded]
        for c in range(256):
            d2 = d1[:] + unknown_string + chr(c)
            c2 = oracle(d2)[:unknown_string_size_rounded]
            if c1 == c2:
                unknown_string += chr(c)
                break
    return unknown_string

print get_unknown_string(encryption_oracle)
# Rollin' in my 5.0
# With my rag-top down so my hair can blow
# The girlies on standby waving just to say hi
# Did you stop? No, I just drove by
