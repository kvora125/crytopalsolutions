from collections import defaultdict

def repeated_blocks(buffer, block_length=16):
    reps = defaultdict(lambda: -1)
    for i in range(0, len(buffer), block_length):
        block = bytes(buffer[i:i + block_length])
        reps[block] += 1
    return sum(reps.values())

max_reps = 0
ecb_ciphertext = None

# The ciphertext is provided in a file named 8.txt
for ciphertext in list(open("8.txt", "r")):
    ciphertext = ciphertext.rstrip()
    reps = repeated_blocks(bytearray(ciphertext))
    if reps > max_reps:
        max_reps = reps
        ecb_ciphertext = ciphertext

ecb_ciphertext
# d880619740a8a19b7840a8a31c810a3d08649af70dc06f4fd5d2d69c744cd283e2dd052f6b641dbf9d11b0348542bb5708649af70dc06f4fd5d2d69c744cd2839475c9dfdbc1d46597949d9c7e82bf5a08649af70dc06f4fd5d2d69c744cd28397a93eab8d6aecd566489154789a6b0308649af70dc06f4fd5d2d69c744cd283d403180c98c8f6db1f2a3f9c4040deb0ab51b29933f2c123c58386b06fba186a
