from django.shortcuts import redirect
from django.views import View
# Importing jwcrypto to generate private and public key pair for RS256 encryption of the JWT token
from jwcrypto.jwk import JWK
# Importing Cryptodome to generate the iv and key for AES-CBC-256 encryption of the JWT token payload
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES


class generateKeys(View):
    def get(self, request):

        # Generating public and private key for JWT token
        private_key, public_key = self.generate_keys()

        # Generating the initialization vector for AES-CBC which is always 16 bytes
        iv = get_random_bytes(AES.block_size)
        
        # Generating the key of 32 bytes for AES-256
        key = get_random_bytes(32)
        
        # Printing all the generated keys in the console log
        print("------------------------------------------------------")
        print("This is the Initialization Vector for the payload encryption. Make this the value of iv variable in the AES encrypt file.")
        print(iv)
        print("------------------------------------------------------")
        print("This is the key for the payload encryption & decryption. Make this the value of key variable in the AES encrypt & decrypt file.")
        print(key)
        print("------------------------------------------------------")
        print("This is the public key for the JWT. Enter the following value in the public_key variable of the validate file.")
        print(public_key)
        print("------------------------------------------------------")
        print("This is the private key for the JWT. Enter the following value in the private_key variable of the create file.")
        print(private_key)
        print("------------------------------------------------------")

        # Redirecting to homepage as this is a view behind the keygen path
        return redirect('homepage')


    # Function for generating the key pair for RS256 encryption/decryption and signature verification
    def generate_keys(self):
        jwk = JWK.generate(
            kty="RSA",
            size=2048,
            alg="RS256",
            use="sig",
            kid="870",
        )
        return jwk.export_private(as_dict=True), jwk.export_public(as_dict=True)
    
