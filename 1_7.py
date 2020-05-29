from Crypto.Cipher import AES

obj = AES.new("YELLOW SUBMARINE", AES.MODE_ECB)
# The ciphertext is provided in a file named 7.txt
ciphertext = "".join(list(open("7.txt", "r"))).decode("base64")
plaintext = obj.decrypt(ciphertext)
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
