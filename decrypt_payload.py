import sys
import base64 as b64

if len(sys.argv) < 2:
    print("Usage : python decrypter.py <encrypted file> <output file>")
    sys.exit()

file_name = sys.argv[1]
out = sys.argv[2]

print("Decypting %s"%(file_name))

file = open(file_name,'rb')
data = b64.b64decode(file.read())
file.close()

print("[*]Payload decrypted!")
print("[*]Outpting decypted payload to %s"%(out))

file2 = open(out,'wb')
file2.write(data)
file2.close()

print("[*]Decypted version of %s saved as %s"%(file_name,out))
