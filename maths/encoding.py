from hashlib import blake2s, blake2b

SALT = "secret"

def positive_hash(value: str) -> str:
    # Make hash
    file_id = blake2s(value.encode())
    file_hs = file_id.digest().hex()
    return file_hs


def letter_hash(value: str) -> str:
    # Create a hash object using BLAKE2b algorithm
    hash_obj = blake2b(SALT.encode())

    # Update the hash object with the text
    hash_obj.update(value.encode())

    # Get the raw bytes of the hash value
    hash_bytes = hash_obj.digest()

    # Convert the bytes to a base-26 string (using only letters)
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    hash_code = ''
    for b in hash_bytes:
        hash_code += alphabet[b % 26]
    return hash_code
