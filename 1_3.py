def score(s):
    # Hacky (and incorrect) way to determine whether a piece of text is in english.
    freq = {}
    freq[' '] = 700000000
    freq['e'] = 390395169
    freq['t'] = 282039486
    freq['a'] = 248362256
    freq['o'] = 235661502
    # ...
    freq['z'] = 2456495
    score = 0
    for c in s.lower():
        if c in freq:
            score += freq[c]
    return score

def break_single_key_xor(b1):
    max_score = None
    english_plaintext = None
    key = None

    for i in range(256):
        b2 = [i] * len(b1)
        plaintext = bytes(xor(b1, b2))
        pscore = score(plaintext)

        if pscore > max_score or not max_score:
            max_score = pscore
            english_plaintext = plaintext
            key = chr(i)
    return key, english_plaintext

b1 = bytearray.fromhex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
print break_single_key_xor(b1)
# ('X', "Cooking MC's like a pound of bacon")
