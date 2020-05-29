key = bytes(random_key(AES.block_size))

def create_admin_profile():
    block_size = get_block_size(profile_for)

    # Let's make the length of "email=...&uid=10&role=" a multiple of block_size
    # so that "user" is block aligned
    mandatory_bytes = "email=&uid=10&role="
    remaining_bytes = (len(mandatory_bytes) / block_size + 1) * block_size
    email_len = remaining_bytes - len(mandatory_bytes)
    email = "A" * email_len
    profile_prefix = profile_for(bytearray(email))[:remaining_bytes]

    # Let's make the length of "email=..." a multiple of block_size so that
    # the rest of the user inputted email is block aligned
    mandatory_bytes = "email="
    remaining_bytes = (len(mandatory_bytes) / block_size + 1) * block_size
    email_len = remaining_bytes - len(mandatory_bytes)
    email = "A" * email_len
    email += pad_pkcs7("admin", block_size)
    profile_postfix = profile_for(email)[
        remaining_bytes:remaining_bytes + block_size
    ]

    profile = profile_prefix + profile_postfix
    return bytes(dec_profile(profile))

create_admin_profile()
# 'email=AAAAAAAAAAAAA&uid=10&role=admin'
