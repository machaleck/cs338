#Written by Kyle Machalec
import hashlib
import binascii
import argparse
import sys
import random

parser = argparse.ArgumentParser()
parser.add_argument("-p1","--passwords1", action="store_true", help="cracks the passwords from passwords1.txt")
parser.add_argument("-p2","--passwords2", action="store_true", help="cracks the passwords from passwords2.txt")
parser.add_argument("-p3","--passwords3", action="store_true", help="cracks the passwords from passwords3.txt")
if (len(sys.argv) == 1):
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

def hashify(word):
    password = word # type=string
    encoded_password = password.encode('utf-8') # type=bytes
    hasher = hashlib.sha256(encoded_password)
    digest = hasher.digest() # type=bytes
    digest_as_hex = binascii.hexlify(digest) # weirdly, still type=bytes
    digest_as_hex_string = digest_as_hex.decode('utf-8') # type=string
    return digest_as_hex_string

# Part 1 ---------------------------------------------------------------------
dict = {}
def build_hash_word_dictionary(): 
    '''
    builds a dictionary, key is hash, value is potential one word password
    returns the number of hashes computed
    '''
    hashes_computed = 0
    words = [line.strip().lower() for line in open('words.txt')]
    for word in words:
        hash = hashify(word)
        hashes_computed += 1
        if hash not in dict:
            dict[hash] = word
    return hashes_computed

if (args.passwords1):
    passwords_cracked = 0

    users = [line.split(":") for line in open('passwords1.txt')]
    hashes_computed = build_hash_word_dictionary()

    with open("cracked1.txt", 'w') as f:
        for user in users:
            username = user[0]
            user_hash = user[1]
            if user_hash in dict:
                f.write(username + ":" + dict[user_hash] + "\n")
                passwords_cracked += 1
    print("Hashes computed: " + str(hashes_computed))
    print("Passwords cracked: " + str(passwords_cracked))

# Part 2 ---------------------------------------------------------------------
if (args.passwords2):
    hashes_computed = 0
    passwords_cracked = 0

    words = [line.strip().lower() for line in open('words.txt')]
    users = [line.split(":") for line in open('passwords2.txt')]
    password_dict = {}
    with open("cracked2.txt", 'w') as f:
        for user in users:
            password_dict[user[1]] = user[0]
        while(passwords_cracked < 50):
            word1, word2 = random.choices(words, k=2)
            combined_word = word1 + word2
            possible_hash = hashify(combined_word)
            hashes_computed += 1
            if possible_hash in password_dict:
                passwords_cracked += 1
                print("Found: " + str(passwords_cracked) + " " + password_dict[possible_hash] + ":" + combined_word + "\n")
                f.write(password_dict[possible_hash] + ":" + combined_word + "\n")
    print("Hashes computed: " + str(hashes_computed))
    print("Passwords cracked: " + str(passwords_cracked))

# Part 3 ---------------------------------------------------------------------
if (args.passwords3):
    hashes_computed = 0
    passwords_cracked = 0

    words = [line.strip().lower() for line in open('words.txt')]
    users = [line.split(":") for line in open('passwords3.txt')]
    with open("cracked3.txt", 'w') as f:
        for user in users:
            username = user[0]
            salt = user[1].split("$")[2]
            user_hash = user[1].split("$")[3]
            
            for word in words:
                possible_hash = hashify(salt + word)
                hashes_computed += 1
                if possible_hash == user_hash:
                    f.write(username + ":" + word + "\n")
                    passwords_cracked += 1
                    break
    print("Hashes computed: " + str(hashes_computed))
    print("Passwords cracked: " + str(passwords_cracked))
