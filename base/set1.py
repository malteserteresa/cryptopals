# base64 is longer because it does something in three not four, utf 7 
# hex is base 16: 0 1 2 3 4 5 6 7 8 9 A B C D E F. Each hex digit reflects a 4-bit binary sequence.
# and you represent an 8 bit number with two hex digits 
# nibble is a group of 4 bits
# base64_chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + "+/"

import base64
import math
import string
from collections import Counter, OrderedDict

from tqdm import trange

def hex2base(text):
    """ Answer to challenge 1 """
    return base64.b64encode(bytes.fromhex(text.encode('utf-8').hex())).decode('ASCII')

def xor(string1, string2):
    """ Answer to challenge 2 """
    return hex(int(string1, 16) ^ int(string2, 16))

def break_single_byte_cipher(text): 
    """ Answer to challenge 3 """
    lowest_difference = math.inf
    encryption_key = ''
    plain_text = ''

    for key in string.printable:
        current_plain_text = _decrypt(text, key)
        current_difference = _difference(current_plain_text)
        
        if current_difference < lowest_difference:
            lowest_difference = current_difference
            encryption_key = key
            plain_text = current_plain_text

    
    # return encryption_key, plain_text
    return encryption_key

def _decrypt(text, key):
    key = key.encode('utf-8').hex()
    text = text.hex()
    decrypted_string = ''
    for j in range(0, len(text), 2):
        xor_value = int(text[j:j+2], 16) ^ int(key, 16) 
        decrypted_string += chr(xor_value)
    return decrypted_string


def _difference(text):
    counter = Counter(text.upper())
    ALPHABET = string.ascii_letters + ' '
    LETTER_FREQUENCY = {'E' : 12.0,
                        'T' : 9.10,
                        'A' : 8.12,
                        'O' : 7.68,
                        'I' : 7.31,
                        'N' : 6.95,
                        'S' : 6.28,
                        'R' : 6.02,
                        'H' : 5.92,
                        'D' : 4.32,
                        'L' : 3.98,
                        'U' : 2.88,
                        'C' : 2.71,
                        'M' : 2.61,
                        'F' : 2.30,
                        'Y' : 2.11,
                        'W' : 2.09,
                        'G' : 2.03,
                        'P' : 1.82,
                        'B' : 1.49,
                        'V' : 1.11,
                        'K' : 0.69,
                        'X' : 0.17,
                        'Q' : 0.11,
                        'J' : 0.10,
                        'Z' : 0.07,
                        ' ': 20.0,
                        ':': 0.02 }
    total = 0
    for letter in ALPHABET:
        total += abs(counter.get(letter.upper(), 0) * 100 / len(text) - LETTER_FREQUENCY[letter.upper()])

    return total / len(ALPHABET)


def decrypt_file(location):
    with open(location, 'rb') as file:
        encrypted_text = file.read()
   
    return break_single_byte_cipher(encrypted_text)
    

def repeating_key_xor(text, key):
    key = key.encode('utf-8').hex()
    text = text.hex()
    encrypted_string = ''
    for i in range(0, len(text), 2):
        xor_value = int(text[i:i+2], 16) ^ int(key[i % len(key): i % len(key) + 2], 16)
        encrypted_string += chr(xor_value)
    return encrypted_string

def calculate_hamming_distance_from_string(string1, string2):
    string1 = ' '.join(f'{x:08b}' for x in bytes(string1, 'utf-8'))
    string2 = ' '.join(f'{x:08b}' for x in bytes(string2, 'utf-8'))
    return sum([s1!=s2 for s1,s2 in zip(string1,string2)])


def calculate_hamming_distance_from_int(string1, string2):
    string1 = ' '.join(f'{x:08b}' for x in chr(string1).encode('utf-8'))
    string2 = ' '.join(f'{x:08b}' for x in chr(string2).encode('utf-8'))
    return sum([s1!=s2 for s1,s2 in zip(string1,string2)])

def break_repeating_key_xor(location):
    with open(location, 'rb') as file:
        cipher_text = base64.b64decode(file.read())
    
    all_hamming_distances = {}

    for keysize in range(2, 40):
        hamming_distance = 0
        for n in range(0, len(cipher_text[::keysize])-1):
            hamming_distance += calculate_hamming_distance_from_int(cipher_text[::keysize][n], cipher_text[::keysize][n+1])
        
        average_hamming_distance = hamming_distance / len(cipher_text[::keysize])
        all_hamming_distances[keysize] = average_hamming_distance

    lowest_hamming_distances = sorted(all_hamming_distances, key=lambda key: all_hamming_distances[key])[:1]

    password_guesses = []
    for lowest_distance in lowest_hamming_distances:
        password = ''
        for i in range(0, lowest_distance):
            chunk = cipher_text[i::lowest_distance]
            password += break_single_byte_cipher(chunk)
        
        password_guesses.append(password)
    
    print(password_guesses)



#print(break_single_byte_cipher('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'))
#print(break_repeating_key_xor('./challenge6.txt'))

with open('./challenge6.txt', 'rb') as file:
        cipher_text = base64.b64decode(file.read())
print(repeating_key_xor(cipher_text, 'Terminator X: Bring the noise'))