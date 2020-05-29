def unshift_right_xor(value, shift):
    result = 0
    for i in range(32 / shift + 1):
        result ^= value >> (shift * i)
    return result

# Borrowed from https://jazzy.id.au/2010/09/22/cracking_random_number_generators_part_3.html
def unshift_left_mask_xor(value, shift, mask):
    result = 0
    for i in range(0, 32 / shift + 1):
        part_mask = (0xffffffff >> (32 - shift)) << (shift * i)
        part = value & part_mask
        value ^= (part << shift) & mask
        result |= part
    return result

def untemper(y):
    value = y
    value = unshift_right_xor(value, 18)
    value = unshift_left_mask_xor(value, 15, 4022730752)
    value = unshift_left_mask_xor(value, 7, 2636928640)
    value = unshift_right_xor(value, 11)
    assert temper(value) == y
    return value

def copy_MT19937_prng(prng):
    untempered_values = []
    for i in range(624):
        untempered_values.append(untemper(prng.extract_number()))
    copied_prng = MT19937.create_from_state(untempered_values)
    return copied_prng

def assert_prngs_equal(prng1, prng2):
    for _ in range(1000):
        assert prng1.extract_number() == prng2.extract_number()

prng = MT19937(19) # Arbitrary seed
copied_prng = copy_MT19937_prng(prng)
assert_prngs_equal(prng, copied_prng)
