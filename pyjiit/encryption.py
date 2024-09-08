from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import json
import base64
import pyjiit.utils

IV = b"dcek9wb8frty1pnm"

def generate_key(date=None) -> bytes:
    return ('qa8y' + pyjiit.utils.generate_date_seq(date) + 'ty1pn').encode()

def generate_local_name(date=None) -> str:
    name_bytes = (pyjiit.utils.get_random_char_seq(4) + pyjiit.utils.generate_date_seq(date) + pyjiit.utils.get_random_char_seq(5)).encode()
    
    return base64.b64encode(encrypt(name_bytes)).decode()


def get_crypt(key: bytes, iv: bytes):
    return AES.new(key, AES.MODE_CBC, iv)

def decrypt(data: bytes) -> bytes:
    crypt = get_crypt(generate_key(), IV)
    return unpad(crypt.decrypt(data), 16)

def encrypt(data: bytes) -> bytes:
    crypt = get_crypt(generate_key(), IV)
    return crypt.encrypt(pad(data, 16))

def deserialize_payload(payload: str, is_json=False) -> dict | str:
    pbytes = base64.b64decode(payload)
    raw = decrypt(pbytes)
    
    return json.loads(raw)


def serialize_payload(payload: dict) -> str:
    raw = json.dumps(payload, separators=(',', ':')).encode()
    pbytes = encrypt(raw)

    return base64.b64encode(pbytes).decode()


if __name__ == "__main__":
    import sys
    print(deserialize_payload(sys.argv[1], True))

