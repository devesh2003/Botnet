import base64 as b64
import sys

if len(sys.argv) < 2:
    print("Usage : python encryptor.py <file to encrypt> <output file>")
    sys.exit()

out = sys.argv[2]
file_name = sys.argv[1]

print("[*]Starting enctyption for %s"%(file_name))

file = open(file_name,'rb')
data = b64.b64encode(file.read())
file.close()

print("[*]Encryption Completed!")
print("[*]Outputing file to %s..."%(out))

file2 = open(out,'wb')
file2.write(data)
file2.close()

print("[*] Encrypted version of %s saved as %s"%(file_name,out))
