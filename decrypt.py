#!/usr/bin/python2.7

from __future__ import division
import subprocess, os, re, sys, string
from tempfile import NamedTemporaryFile

def istext(filename):
    s = readfile(filename)
    text_characters = "".join(map(chr, range(32, 127)) + list("\n\r\t\b"))
    _null_trans = string.maketrans("", "")
    if not s:
        # Empty files are considered text
        return True
    if "\0" in s:
        # Files with null bytes are likely binary
        return False
    # Get the non-text characters (maps a character to itself then
    # use the 'remove' option to get rid of the text characters.)
    t = s.translate(_null_trans, text_characters)
    # If more than 30% non-text characters, then
    # this is considered a binary file
    if float(len(t)) / float(len(s)) > 0.30:
        return False
    return True

def readfile(name):
    return open(name, 'r').read()

def process_text(text):
    variants = []
    variants.append(text.replace('\n', ''))
    variants.append(text.replace(' ', ''))
    variants.append(text.replace('\n', '').replace(' ', ''))
    variants.append(re.sub('[\w\d\!\.-]', '', text.replace('\n', '').replace(' ', '')))
    variants.append(re.sub('[\w\d\!\.-]', '', text.replace(' ', '')))
    variants.append(re.sub('[\w\d\!\.-]', '', text.replace('\n', '')))
    variants.append(re.sub('[^\w\d\!\.-]', '', text))
    variants.append(re.sub('[^\w\d]', '', text))
    variants.append(re.sub('[^\d]', '', text))
    return variants

def variant_filename(index):
    return 

cwd = os.path.dirname(os.path.realpath(__file__))
openssl_cyphers = (
    "aes-128-cbc", "aes-128-ecb", "aes-192-cbc", "aes-192-ecb", "aes-256-cbc", "aes-256-ecb",
    "bf", "bf-cbc", "bf-cfb", "bf-ecb", "bf-ofb",
    "camellia-128-cbc", "camellia-128-ecb", "camellia-192-cbc", "camellia-192-ecb", "camellia-256-cbc", "camellia-256-ecb",
    "cast", "cast-cbc", "cast5-cbc", "cast5-cfb", "cast5-ecb", "cast5-ofb",
    "des", "des-cbc", "des-cfb", "des-ecb", "des-ede", "des-ede-cbc", "des-ede-cfb", "des-ede-ofb", "des-ede3", "des-ede3-cbc", "des-ede3-cfb", "des-ede3-ofb", "des-ofb", "des3", "desx",
    "rc2", "rc2-40-cbc", "rc2-64-cbc", "rc2-cbc", "rc2-cfb", "rc2-ecb", "rc2-ofb",
    "rc4", "rc4-40",
    "seed", "seed-cbc", "seed-cfb", "seed-ecb", "seed-ofb"
)
cyrillic_encodings = ("mac_cyrillic", "iso8859_5", "cp855", "cp866", "cp1251", "koi8_r")
input_file = "cyphertext.bin"
key_file = "key.txt"
print_all = True
output_file = NamedTemporaryFile(delete=False)
output_file.close()

# trim whitespaces
key_contents = readfile(key_file).strip()

for cypher in openssl_cyphers:
    for encoding in cyrillic_encodings:
        text = key_contents.decode('utf-8').encode(encoding)
        variants = process_text(text)
        for v_index, v in enumerate(variants):
            cmd = ("openssl", cypher, "-d", "-in", input_file, "-out", output_file.name, "-k", v)
            child = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
            data = child.communicate()
            #if child.returncode == 0 or print_all:
            if istext(output_file.name):
                decrypted = readfile(output_file.name)
                decrypted = decrypted.decode(encoding)
                print "[var%d, %s, %s]\n%s\n%s" % (v_index, encoding, cypher, decrypted, '-' * 50)
