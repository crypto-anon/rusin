#!/usr/bin/python2.7

import subprocess, os, re

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
    return cwd + '/output/var_' + str(index) + '.txt'

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
input_file = "cyphertext.bin"
output_file = "result.txt"
key_file = "key.txt"
print_all = True

if not os.path.exists(cwd + '/output'):
    os.mkdir(cwd + '/output')
if not os.path.exists(cwd + '/input'):
    os.mkdir(cwd + '/input')

# trim whitespaces
key_contents = readfile(key_file)
#key_file_trimmed = cwd + '/output/key_trimmed.txt'
#f = open(key_file_trimmed, 'w')
#f.write(key_contents.strip())
#f.close()

variants = process_text(key_contents)
for variant_index, variant in enumerate(variants):
    with open(variant_filename(variant_index), 'w') as f:
        f.write(variant)

for cypher in openssl_cyphers:
    for variant_index, variant in enumerate(variants):
        variant_file = variant_filename(variant_index)

        cmd = ("openssl", cypher, "-d", "-in", input_file, "-out", output_file, "-k", readfile(variant_file))
        child = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
        data = child.communicate()
        if child.returncode == 0 or print_all:
            print "[var%d, %s]\n%s\n%s" % (variant_index, cypher, readfile(output_file), '-' * 50)
