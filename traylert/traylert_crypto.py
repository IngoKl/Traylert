from Cryptodome.Cipher import AES

def encrypt(data, key):
	cipher = AES.new(key.encode("utf8"), AES.MODE_EAX)
	ciphertext, tag = cipher.encrypt_and_digest(data.encode("utf8"))

	c = {'nonce': cipher.nonce, 'tag': tag, 'ciphertext': ciphertext}

	return c


def decrypt(data, key):
	cipher = AES.new(key.encode("utf8"), AES.MODE_EAX, data['nonce'])
	data_dec = cipher.decrypt_and_verify(data['ciphertext'], data['tag'])

	return data_dec