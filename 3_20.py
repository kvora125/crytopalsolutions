key = random_key(AES.block_size)
FIXED_NONCE = 0
ciphertexts = []
for encoded_plaintext in list(open("20.txt", "r")):
    plaintext = bytearray(encoded_plaintext).decode("base64")
    ciphertexts.append(aes_128_ctr(plaintext, key, FIXED_NONCE))

# Trim the ciphertexts to the length of the least long one
min_ciphertext_length = min(map(len, ciphertexts))
ciphertexts = [bytes(ciphertext[:min_ciphertext_length]) for ciphertext in ciphertexts]
b = bytearray("".join(ciphertexts))
print repr(b)

block_bytes = [[] for _ in range(min_ciphertext_length)]
for i, byte in enumerate(b):
    block_bytes[i % min_ciphertext_length].append(byte)

keys = ""
for bbytes in block_bytes:
    keys += break_single_key_xor(bbytes)[0]
key = bytearray(keys * len(b))
plaintext = bytes(xor(b, key))

print plaintext
# N'm rated "R"...this is a warning, ya better void / PDuz I came back to attack others in spite- ...
