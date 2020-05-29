def aes_128_ecb_enc(buffer, key):
    obj = AES.new(key, AES.MODE_ECB)
    return bytearray(obj.encrypt(bytes(buffer)))

def aes_128_ecb_dec(buffer, key):
    obj = AES.new(key, AES.MODE_ECB)
    return bytearray(obj.decrypt(bytes(buffer)))

def aes_128_cbc_enc(buffer, key, iv):
    plaintext = pad_pkcs7(buffer, AES.block_size)
    ciphertext = bytearray(len(plaintext))
    prev_block = iv
    for i in range(0, len(plaintext), AES.block_size):
        ciphertext[i: i + AES.block_size] = aes_128_ecb_enc(
            xor(plaintext[i: i + AES.block_size], prev_block),
            key,
        )
        prev_block = ciphertext[i: i + AES.block_size]
    return ciphertext

def aes_128_cbc_dec(ciphertext, key, iv):
    plaintext = bytearray(len(ciphertext))
    prev_block = iv
    for i in range(0, len(ciphertext), AES.block_size):
        plaintext[i: i + AES.block_size] = xor(
            aes_128_ecb_dec(bytes(ciphertext[i: i + AES.block_size]), key),
            prev_block
        )
        prev_block = ciphertext[i: i + AES.block_size]
    return unpad_pkcs7(plaintext)

plaintext = bytearray("Hello my name is Michael")
iv = bytearray([chr(0)] * AES.block_size)
key = "YELLOW SUBMARINE"

assert aes_128_cbc_dec(aes_128_cbc_enc(plaintext, key, iv), key, iv) == plaintext
# Assertion passes - encryption and decryption are correct
# The ciphertext are provided in a file named 10.txt
ciphertext = bytearray("".join(list(open("10.txt", "r"))).decode("base64"))
aes_128_cbc_dec(ciphertext, key, iv)
# I'm back and I'm ringin' the bell
# A rockin' on the mike while the fly girls yell
# In ecstasy in the back of me
# Well that's my DJ Deshay cuttin' all them Z's
# Hittin' hard and the girlies goin' crazy
# Vanilla's on the mike, man I'm not lazy.

# I'm lettin' my drug kick in
# ...
