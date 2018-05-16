import rsa
import sys

# this is a test file showing how to generate key pairs with this rsa package

pubkeyfile = sys.argv[1]
privkeyfile = sys.argv[2]

(pubkey, privkey) = rsa.newkeys(512)

file = open(pubkeyfile, 'w')
pubpem = str(pubkey)
file.write(pubpem)

file = open(privkeyfile, 'w')
privpem = str(privkey)
file.write(privpem)

# this shows how to create a digsig with rsa hashed with SHA-1

message = 'you' + 'themthemthemthem' + str(1)
message = message.encode('utf8')
sig = rsa.sign(message, privkey, 'SHA-1')
signature = str(sig)
print(signature)
