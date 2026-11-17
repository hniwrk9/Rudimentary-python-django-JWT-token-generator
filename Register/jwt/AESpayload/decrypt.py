# Importing the built-in ast to convert string into dictionary
import ast
# Importing Cryptodome for decrypting the JWT payload data with AES-256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def load_decrypt(payload):
    
    # Enter the key from the keygen here
    key = b'\x86y]\x9b0\x84\xc5\xf5G,\x15D3D\x99\xf3|Bf)\xf5F\xbbAJ/<\x01\xc6v8U'

    # Initialization vector is extracted from the encrypted payload
    iv = payload[:AES.block_size]

    # The cipher will decrypt the our AES-256-CBC encrypted data with the key and the iv
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # The encrypted data is extracted from the payload and decrypted with the cipher
    decrypted_padded = cipher.decrypt(payload[AES.block_size:])

    # The decrypted data is padded. Using unpad to remove the padding. This will return byte data
    decrypted = unpad(decrypted_padded, AES.block_size)
    
    # Converting the byte data back into the string
    decrypted_text = decrypted.decode()

    # Converting the string back into the original dictionary
    payredict = ast.literal_eval(decrypted_text)

    # Function returns the decrypted data in dictionary format for further validation and processing
    return payredict
