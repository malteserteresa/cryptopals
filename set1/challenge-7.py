import base64
from Crypto.Cipher import AES

def decrypt(data, password):
    password = password.encode('utf8')

    cipher = AES.new(password, AES.MODE_ECB)
    plain_text = cipher.decrypt(data)
    return plain_text.decode('utf8').rstrip('\0')

with open('7.txt', 'rb') as file:
    cipher_text = base64.b64decode(file.read())

plain = decrypt(cipher_text, "YELLOW SUBMARINE")

print(plain)