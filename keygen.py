import rsa
import sys

# this is a tool to generate public/private key pairs for use by the
# multiple nodes/users in the blockchain project
def create_keys():
    pubkeyfile = sys.argv[1]
    privkeyfile = sys.argv[2]
    (pubkey, privkey) = rsa.newkeys(512)
    with open(pubkeyfile, "w") as text_file:
        text_file.write(pubkey.save_pkcs1().decode('utf8'))
    with open(privkeyfile, "w") as text_file:
        text_file.write(privkey.save_pkcs1().decode('utf8'))

# this shows how to create a digsig with rsa hashed with SHA-1
"""
message = 'you' + 'themthemthemthem' + str(1)
message = message.encode('utf8')
sig = rsa.sign(message, privkey, 'SHA-1')
signature = str(sig)
print(signature)
"""

create_keys()
