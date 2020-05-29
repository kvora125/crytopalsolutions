lines = [
    "Burning 'em, if you ain't quick and nimble\n",
    "I go crazy when I hear a cymbal",
]

text = "".join(lines)
key = bytearray("ICE" * len(text))
plaintext = bytes(xor(bytearray(text), key))
plaintext.encode("hex")
# 0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f
# The ciphertext is provided in a file named 6.txt
b = bytearray("".join(list(open("6.txt", "r"))).decode("base64"))

normalized_distances = []
for KEYSIZE in range(2, 40):
    b1 = b[: KEYSIZE]
    b2 = b[KEYSIZE: KEYSIZE * 2]
    b3 = b[KEYSIZE * 2: KEYSIZE * 3]
    b4 = b[KEYSIZE * 3: KEYSIZE * 4]

    normalized_distance = float(
        hamming_distance(b1, b2) +
        hamming_distance(b2, b3) +
        hamming_distance(b3, b4)
    ) / (KEYSIZE * 3)

    normalized_distances.append(
        (KEYSIZE, normalized_distance)
    )

normalized_distances = sorted(normalized_distances, key=lambda (\_, y): y)
# [(2, 2.0), (3, 2.6666666666666665), (29, 2.793103448275862), ...]
for KEYSIZE, _ in normalized_distances[:5]:
    block_bytes = [[] for _ in range(KEYSIZE)]
    for i, byte in enumerate(b):
        block_bytes[i % KEYSIZE].append(byte)

    keys = ""
    for bbytes in block_bytes:
        keys += break_single_key_xor(bbytes)[0]

    key = bytearray(keys * len(b))
    plaintext = bytes(xor(b, key))

    print keys
    print KEYSIZE
    print plaintext

# Some nonsense ...

# Terminator X: Bring the noise
# 29
# I'm back and I'm ringin' the bell
# A rockin' on the mike while the fly girls yell
# In ecstasy in the back of me
# Well that's my DJ Deshay cuttin' all them Z's
# Hittin' hard and the girlies goin' crazy
# Vanilla's on the mike, man I'm not lazy.
#
# I'm lettin' my drug kick in
# It controls my mouth and I begin
# To just let it flow, let my concepts go
# My posse's to the side yellin', Go Vanilla Go!
# ...

# More nonsense ...
