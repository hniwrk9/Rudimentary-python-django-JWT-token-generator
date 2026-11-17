# Importing jwt module for jwt token verification and JSON serialization of the public key
from jwt import JWT, jwk_from_dict
# Importing datetime for checking custom expiry in the payload
from datetime import datetime, date
# Importing hasher to verify the hash of the Staff ID
from django.contrib.auth.hashers import check_password
# Importing User to fetch data for verification and checking access level
from Register.models import User
# Importing the AES decyprtion script for the encrypted payload
from .AESpayload.decrypt import load_decrypt
# Importing base64 to decode encrypted payload
import base64

# Create an instance of the class JWT from the module jwt
jwt = JWT()

def validate(token, data_request=False):

    # Enter the public key from the keygen here. This is a dictionary containing JWK data
    public_key = {'kty': 'RSA', 'use': 'sig', 'alg': 'RS256', 'kid': '870', 'n': 'wO7dT12ziaegL4M11r_rZghLHmhV7tXZhBETC9dFqErMkUA3OTONWkEXEUoDyL2wUuBUPSn7Ry5O61mwIOd9Fwqud9unb24vbfYIxp0E33GXVOUZxNJXsqYhvSrrH2RyMEn1Y49EgSllG9Gt4Zk2_6c3Bqn2NR6pTqowCC1De0ss-l-WjwpsNrUeJkyWHhqXTfBFqjJA9JLPc7sicgCRBxxieW8dmNA1XtvmlTfcNahQRJ1dn93KitXqND5Yae3gQRbN9y_bWB0HR6w5cTLI1wqcUIZ_26-I6DtTacJqyRemKh_OxG_QbTFPQjuB14TIhF8iEt5vLBs_9gZVgZ5TVQ', 'e': 'AQAB'}

    # Converting the JWK data from the dictionary above into a JWK object
    jwk = jwk_from_dict(public_key)

    try:
        # Verifying the signature and decoding the JWT with the public key
        decoded = jwt.decode(token, jwk)
    except:
        # If verification or decryption fails, an error message and a false status are returned in a dictionary
        error_msg = "Bad token! Contact an administrator"
        validation_status = {
            'status' : False,
            'error_msg' : error_msg,
        }
        return validation_status
    
    try:
        # The base64 encoded payload string is decoded and converted back into a byte
        encrypted_data = base64.b64decode(bytes(decoded.get('payload'),'utf-8'))
    except:
        # If byte conversion fails, an error message and a false status are returned in a dictionary 
        error_msg = "Bad token! Contact an administrator"
        validation_status = {
            'status' : False,
            'error_msg' : error_msg,
        }
        return validation_status
    
    try:
        # The encrypted byte data is decrypted with the decryption script and converted into a dictionary
        payredict = load_decrypt(encrypted_data)
    except:
        # If payload decryption script fails, an error message and a false status are returned in a dictionary
        error_msg = "Bad token! Contact an administrator"
        validation_status = {
            'status' : False,
            'error_msg' : error_msg,
        }
        return validation_status
    
    # Getting the expected values from the decrypted dictionary and assigning variables
    ran = payredict.get('user_id')
    user_hash = payredict.get('user_hash')
    e = payredict.get('e')

    # Fetching the User object with the unique random user ID from the decrypted data
    user = User.get_user_by_ran(ran)

    # Checking the Staff ID hash from the decrypted data against the inherited staff ID from the User object
    try:
        hash_check = check_password(user.staff.csid, user_hash)
    except:
        # If Staff ID hash check fails, an error message and a false status are returned in a dictionary 
        error_msg = "Bad token! Contact an administrator"
        validation_status = {
            'status' : False,
            'error_msg' : error_msg,
        }
        return validation_status
    
    # Converting the expiry date from the decrypted data into date format
    exp = datetime.strptime(e, '%Y-%m-%d').date()

    # Checking if the current date is past the expiry date
    if date.today() <= exp:

        # Checking if the Staff ID hash check was successful
        if hash_check:

            # Checking if the data_request parameter is passed as True to return the unique random user ID for further processing
            if data_request:
                validation_status = {
                'status' : True,
                'ran': ran,
                }
                return validation_status
            
            # Returning True status to confirm data verification was successful
            else:
                validation_status = {
                'status' : True,
                }
                return validation_status
            
        # Returing error message if decrypted Staff ID hash could not be verified
        else:
            error_msg = "Invalid token! Please contact an administrator"   
            validation_status = {
                'status' : False,
                'error_msg' : error_msg,
            }
            return validation_status

    # Returing error message if token is expired
    else:
        error_msg = "Invalid token! Please contact an administrator"
        validation_status = {
            'status' : False,
            'error_msg' : error_msg,
        }
        return validation_status









