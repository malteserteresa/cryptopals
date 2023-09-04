import base64
from collections import Counter


with open('8.txt', 'r') as file:
    cipher_text = file.readlines()

print(cipher_text)


for j, line in enumerate(cipher_text):
    line = line.strip('\n')
    chunks = [line[i:i+16] for i in range(0, len(line), 16)]
    repeated_chunks = Counter(chunks)
    print(repeated_chunks)
