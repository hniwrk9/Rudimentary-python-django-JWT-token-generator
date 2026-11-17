# Importing jwt module for jwt token generation and JSON serialization of the private key
from jwt import JWT, jwk_from_dict
# Importing datetime for adding expiry
from datetime import date, timedelta
# Importing hasher to generate a new hash of the Staff ID
from django.contrib.auth.hashers import make_password
# Importing User to fetch data for encryption
from Register.models import User
# Importing the AES encryption script for the payload data
from .AESpayload.encrypt import load_encrypt
# Importing base64 to encode the AES encrypted data
import base64

# Create an instance of the class JWT from the package jwt
jwt = JWT()

def create(ran):

    # Fetching the User object with the randomly generated user ID fetched in the ntoken view
    user = User.get_user_by_ran(ran)

    # IDs from the User table are assigned variables. The Staff ID is hashed for added protection (Not really)
    user_id = user.ran
    user_hash = make_password(user.staff.csid)

    # Expiry date is converted into a string and sent in the encrypted payload
    e = str(date.today() + timedelta(days=5))

    # Making a dictionary of the data fetched above
    paydict = {
    'user_id' : user_id,
    'user_hash' : user_hash,
    'e': e
    }

    # Encrypting the dictionary with the encryption script. The data will be converted into a byte before encryption.
    # Byte data is not JSON serializable. It is converted into a string with base64 encoding.
    encrypted_data = str(base64.b64encode(load_encrypt(paydict)), 'utf-8')

    # This is a hardcoded variable to show which system is generating the JWT token. It can be changed during implementation to fetch a dynamic value
    sys = 1

    # Making a dictionary to be serialized for token generation
    payload = {
        'sys': sys,
        'payload': encrypted_data,
    }

    # Enter the private key from the keygen here. This is a dictionary containing JWK data
    private_key = {'kty': 'RSA', 'use': 'sig', 'alg': 'RS256', 'kid': '870', 'n': 'wO7dT12ziaegL4M11r_rZghLHmhV7tXZhBETC9dFqErMkUA3OTONWkEXEUoDyL2wUuBUPSn7Ry5O61mwIOd9Fwqud9unb24vbfYIxp0E33GXVOUZxNJXsqYhvSrrH2RyMEn1Y49EgSllG9Gt4Zk2_6c3Bqn2NR6pTqowCC1De0ss-l-WjwpsNrUeJkyWHhqXTfBFqjJA9JLPc7sicgCRBxxieW8dmNA1XtvmlTfcNahQRJ1dn93KitXqND5Yae3gQRbN9y_bWB0HR6w5cTLI1wqcUIZ_26-I6DtTacJqyRemKh_OxG_QbTFPQjuB14TIhF8iEt5vLBs_9gZVgZ5TVQ', 'e': 'AQAB', 'd': 'KZz7uAweVuEEYGsdGDIx_EJqrWbUrhyK-3zRTlsCx79Ga0feAWT4ppBmgNCli006tE11bfHZpGs9E283WYmEhg1EP07tyM-LxFxuXSRt8iHmgaWejsDNsJc7rLkOmKlKJdc16eDzZiZ_C-aIaiHpZm_zIulS1PdFjlWP4ZudtABNie3C-rtfVlLro4otJ-y-pm7W20MGJ25uAhBL8k3pz2VAOuVjsLEAU6yCPFpTDIFT2jZkZu1I85ffWocvqVrPbAP2L59vv4_WyzQ7YRXTA78Zgu8nmtkC3eAWRlM70wF1Wv7L2XhmO04XVMtAFwUS7TRTVXXL9cINv54SiKPWiw', 'p': '5ZbO60YLtweyg8ULfrXBzji2662RpB85Qa3n8vBU57FfDWObmajt5MQ1nUaQwLE3RYJ5oAAiWscfMAq6P9rqTyXJnMTkxtOKQ2h0G0pLlBnKmNk8bfPeblIMkUFUKhj66VKnsK-dlofrZfIbNNt5siX9lYklUYysmcct4Z03gV8', 'q': '1yCRtkvgj8qFD-0m0ZcOL_AZC9tJyvGAP3H8eifooyBimMnXfTLRFRuweaDdLY70-FSMiN8dhAzmtjTzt1UBuT4VsGliC-gIwdfB2uuYy4slPdzJRuM28_ouI9Q-gsljqR7JC_miB9f-B1L1f7Kqem7NejbPqiZRhweqtkpNY8s', 'dp': 'Wmn-iNbn7CeC3LOvqDHJ5f2dw8hxz5FgSgZDjv-oYCoQxcQRVf0Z2nqOpqZQgSIJIz2TyjfjT56VIKVI3bbHiW3XLP65HbfW_l7XQpwKkYNqrrD2RFLCqO1094sjqwR1Y4didIlkZRCX2mjy3-kCzu55I_eDk87zdgfjgLMaVb8', 'dq': 'C9SKrs-1ZbLpZlrQS65W5WP6vKAuiq6FMvf9vmn7bR0WzvgqlYP544NGTSn_f8Xgytc7cztx0BU1iseWr3pJQfqcDrt83NLByIco7fUOzgK05ZYCq5dLKleTufyuA1s309ERlUsBEhVaruRtA7y7i0gUnKfu-5hn21kcljG318k', 'qi': '0yhEM9XePjZO-tlDJIXBnYXMeKXNo1GEheu_ssdjLwvg8szF3KGhVmlKs9pnRjANKQGXVCm-_Ta2h97PSk2mLkWwbWtmoW5Ar8ckUClFucTR34JnNdG8bOzPsBp-POOqAj3tAo2LDjp_siulOp9LJk2d1J1cS6Bz7GpbonyWVqk'}

    # Converting the JWK data from the dictionary above into a JWK object
    jwk = jwk_from_dict(private_key)

    # The JWT token is created using the encode method in the jwt instance with the RS256 algorithm and the JWK object
    # The token has encrypted payload data and is signed to make it tamper proof
    token = jwt.encode(payload, jwk, alg="RS256")

    # The JWT token is returned
    return token

    
    
# This is another way of encoding and decoding. A local function can be made to make the JWK object and create the JWT token
# If there was more functionality added to this scrypt package then this would have been a better method to simplify code

# def encode(self, data, key):
#     jwk = jwk_from_dict(key)
#     return jwt.encode(data, jwk, alg="RS256")
        




