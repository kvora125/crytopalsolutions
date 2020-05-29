from random import randint

def random_key(length):
    key = bytearray(length)
    for i in range(length):
        key[i] = chr(randint(0, 255))
    return key

print repr(random_key(16))
# bytearray(b'\xe0L\xa7\xb3Z\xd6\xc0e\x87vc\xc4*\x96,\x14')
def encryption_oracle(buffer):
    bytes_to_add = randint(5, 10)
    plaintext = pad_pkcs7(
        random_key(bytes_to_add) +
        buffer +
        random_key(bytes_to_add),
        AES.block_size
    )
    key = bytes(random_key(16))
    if randint(0, 1):
        # Return a tuple of the ciphertext and 1 to
        # indicate it has been encrypted in ECB mode
        return aes_128_ecb_enc(plaintext, key), 1
    else:
        iv = random_key(16)
        # Return a tuple of the ciphertext and 0 to
        # indicate it has been encrypted in CBC mode
        return aes_128_cbc_enc(plaintext, key, iv), 0

encryption_oracle(bytearray("My name is Michael"))
# bytearray(b'x\xb5:\xe14\xaf\x10EK\x04[\xd6#\xe5\xf3OClz\x9c\x90\xce^\xfb\xbb\x86\x16\x97\xdcQ\x10\x15'), 1
def is_ecb_mode(buffer, block_size):
    return repeated_blocks(buffer, block_size) > 0

# The ciphertext are provided in a file named 11.txt
plaintext = bytearray("".join(list(open("11.txt", "r"))))
for i in range(1000):
    # ecb_mode is True when the plaintext is encrypted using ECB mode
    ciphertext, ecb_mode = encryption_oracle(plaintext)
    if ecb_mode != is_ecb_mode(ciphertext, AES.block_size):
        print "Detection does not work"
        exit()

print "Detection works"
