import sys
from pathlib import Path
import os
from os.path import expanduser
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


"""

Encrypts files from command line
Using AES encryption in EAX mode in order to check for tampering
Derick Falk

"""

# Checks if keyfile already exists and creats it if it does not
keyfile = Path(expanduser('~') + '\k.key')
if keyfile.is_file():
	file = open(keyfile,'rb')
	key = file.read()
	file.close()
else:
	print(f'Creating key file at {keyfile}')
	key = get_random_bytes(24)
	file_out = open(keyfile,'wb')
	file_out.write(key)
	file_out.close()
	file = open(keyfile,'rb')
	key = file.read()
	file.close()



# Usuage 
if len(sys.argv) < 3:
	print('Program to encrypt or decrypt file using AES')
	print('Usuage: python Efile.py filename [options]')
	print('	Commands:')
	print('		--d, -decrypt    Decrypts file\n\
		--e,  -encrypt    Encrypts file')
	sys.exit(0)
# Encrypt option encrypts a file and saves it with .encrypt extension
if sys.argv[2] == '--e' or sys.argv[2] == '-encrypt':
	# Creates a file object and reads the files data in
	in_file = os.path.abspath(sys.argv[1])
	file = open(in_file,'rb')
	data = file.read()
	file.close()

	# Creates the cipher object and encrypts the data
	cipher = AES.new(key, AES.MODE_EAX)
	ciphertext, tag = cipher.encrypt_and_digest(data)
	file = open(in_file[0:-4] + '.encrypted', 'wb')
	[file.write(x) for x in (cipher.nonce, tag, ciphertext)]
	file.close()

# Decrypt option decrypts a file and saves it with .decrypted extension
elif sys.argv[2] == '--d' or sys.argv[2]=='-decrypt':
	in_file = os.path.abspath(sys.argv[1])
	file = open(in_file, 'rb')
	
	nonce, tag, ciphertext = [file.read(x) for x in (16,16,-1)]
	file.close()
	cipher = AES.new(key,AES.MODE_EAX, nonce)
	data = cipher.decrypt_and_verify(ciphertext,tag)
	file = open(in_file[0:-10] + '.decrypted','wb')
	file.write(data)
	file.close()	

	
