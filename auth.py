import jwt    # PyJWT 
import uuid
import hashlib
from urllib.parse import urlencode

def get_jwt_token(ak, sk, body):
    m = hashlib.sha512()
    m.update(urlencode(body).encode())
    query_hash = m.hexdigest()

    payload = {
        'access_key': ak,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }
        
    return jwt.encode(payload, sk)