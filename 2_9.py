def pad_pkcs7(buffer, block_size):
    if len(buffer) % block_size:
        padding = (len(buffer) / block_size + 1) * block_size - len(buffer)
    else:
        padding = 0
    # Padding size must be less than a byte
    assert 0 <= padding <= 255
    new_buffer = bytearray()
    new_buffer[:] = buffer
    new_buffer += bytearray([chr(padding)] * padding)
    return new_buffer

buffer = bytearray("YELLOW SUBMARINE")
pad_pkcs7(buffer, 20)
# bytearray(b'YELLOW SUBMARINE\x04\x04\x04\x04')
