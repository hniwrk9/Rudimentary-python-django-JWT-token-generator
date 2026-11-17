# Importing Cryptodome for encrypting the JWT payload data with AES-256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad



def load_encrypt(paydict):

    # Enter the key from the keygen here
    key = b'\x86y]\x9b0\x84\xc5\xf5G,\x15D3D\x99\xf3|Bf)\xf5F\xbbAJ/<\x01\xc6v8U'
    # Enter the iv from the keygen here
    iv = b",\x87\x8b\x83\xb0\x1b96\x8e\xe4'\xa6\xd2\x10\x90~"

    # Dictionary of the payload values is converted into a string before it is padded
    payload = str(paydict)

    # The cipher will encrypt the string by utilizing the CBC mode of operation with a 32 byte key and iv. This will encrypt the data with an AES-256-CBC algorithm.
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # String data is converted into byte using the encode() method and padded
    padded_text = pad(payload.encode(), AES.block_size)

    # Padded string is encrypted with the cipher
    encrypted_text = cipher.encrypt(padded_text)

    # Function returns the initialization vector concatenated with the encrypted payload.
    return iv + encrypted_text










