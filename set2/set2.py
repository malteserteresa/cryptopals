import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad



def implement_pkcs7(plaintext, block_size):
    number_of_bytes = len(plaintext)
    if number_of_bytes < block_size:
        padding_required = block_size - number_of_bytes
    else:
        padding_required = number_of_bytes % block_size
    
    return plaintext + b'\x04' * padding_required


# print(repr(implement_pkcs7(b"YELLOW SUBMARINE", 20)))


def encrypt(data, password):
    iv = b'\x00' * AES.block_size
    cipher = AES.new(password.encode('utf-8'), AES.MODE_CBC, iv)
    return base64.b64encode(cipher.encrypt(implement_pkcs7(data, AES.block_size)))

with open('10.txt', 'rb') as file:
    cipher_text = base64.b64decode(file.read())

sample_test = encrypt(cipher_text, "YELLOW SUBMARINE")

# print(plaintext)

def decrypt(data, password):
    iv = b'\x00' * AES.block_size
    cipher = AES.new(password.encode('utf-8'), AES.MODE_CBC, iv)
    return cipher.decrypt(data)

plaintext = decrypt(cipher_text, "YELLOW SUBMARINE")

print(plaintext)