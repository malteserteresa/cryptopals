import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import random
from collections import Counter


def implement_pkcs7(plaintext, block_size):
    number_of_bytes = len(plaintext)
    if number_of_bytes < block_size:
        padding_required = block_size - number_of_bytes
    else:
        padding_required = number_of_bytes % block_size
    
    return plaintext + b'\x04' * padding_required


# print(repr(implement_pkcs7(b"YELLOW SUBMARINE", 20)))
def encrypt_ecb(data, password):
    cipher = AES.new(password, AES.MODE_ECB)
    return cipher.encrypt(pad(data, AES.block_size))

def encrypt_cbc(data, password):
    iv = b'\x00' * AES.block_size
    cipher = AES.new(password, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(data, AES.block_size))

with open('10.txt', 'rb') as file:
    cipher_text = base64.b64decode(file.read())

sample_test = encrypt_cbc(cipher_text, b"YELLOW SUBMARINE")

# print(plaintext)

def decrypt(data, password):
    iv = b'\x00' * AES.block_size
    cipher = AES.new(password, AES.MODE_CBC, iv)
    return cipher.decrypt(data)

plaintext = decrypt(cipher_text, b"YELLOW SUBMARINE")



# challenge 11

# 1. Generate random AES key (16 random bytes)
# 2. funtion to encrypt with random key
# 3. add 5-10 bytes before and after plaintext
# 4. function should enrypt under ecb and cbc randomly
# 5. write another function that says whether the encryption was ecb or cbc

def generate_key():
    return open("/dev/urandom","rb").read(16)

def get_penguin():
    with open('./tux.png', 'rb') as file:
        tux = file.read()

    before = open("/dev/urandom","rb").read(random.randint(5, 10))
    after = open("/dev/urandom","rb").read(random.randint(5, 10))

    return before + tux * 17 + after

def encrypt_at_random():
    plain = get_penguin()
    key = generate_key()

    if random.randint(0, 1) == 1:
        cipher = encrypt_ecb(plain, key)
        mode = 'ecb'
    else:
        cipher = encrypt_cbc(plain, key)
        mode = 'cbc'

    return cipher, mode

def ecb_cbc_oracle():
    cipher_text, correct = encrypt_at_random()
    chunks = []
    for j in range(0, 16):
        chunks += [cipher_text[i:i+16] for i in range(j, len(cipher_text), 16)]

    repeated_chunks = Counter(chunks)
    if all(v == 1 for v in repeated_chunks.values()):
        print('cbc is predicted and correct is', correct)
    else:
        print('ecb is predicted and correct is', correct)
    #print(type(dict(repeated_chunks)))

ecb_cbc_oracle()