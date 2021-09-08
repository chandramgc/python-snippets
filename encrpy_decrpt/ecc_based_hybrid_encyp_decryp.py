from tinyec import registry
from Crypto.Cipher import AES
import hashlib
import secrets
import binascii


def encrypt_AES_GCM(msg, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM)
    ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
    return (ciphertext, aesCipher.nonce, authTag)


def decrypt_AES_GCM(ciphertext, nonce, authTag, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
    plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
    return plaintext



def ecc_point_to_256_bit_key(point):
    sha = hashlib.sha256(int.to_bytes(point.x, 32, 'big'))
    sha.update(int.to_bytes(point.y, 32, 'big'))
    return sha.digest()


# curve = registry.get_curve('brainpoolP256r1')
curve = registry.get_curve('secp192r1')


def encrypt_ECC(msg, pubKey):
    ciphertextPrivKey = secrets.randbelow(curve.field.n)
    sharedECCKey = ciphertextPrivKey * pubKey
    secretKey = ecc_point_to_256_bit_key(sharedECCKey)
    ciphertext, nonce, authTag = encrypt_AES_GCM(msg, secretKey)
    ciphertextPubKey = ciphertextPrivKey * curve.g
    return (ciphertext, nonce, authTag, ciphertextPubKey)


def decrypt_ECC(encryptedMsg, privKey):
    (ciphertext, nonce, authTag, ciphertextPubKey) = encryptedMsg
    sharedECCKey = privKey * ciphertextPubKey
    secretKey = ecc_point_to_256_bit_key(sharedECCKey)
    plaintext = decrypt_AES_GCM(ciphertext, nonce, authTag, secretKey)
    return plaintext


msg_original = "Text to be encrypted by ECC public key and decrypted by its corresponding ECC private key"
msg = msg_original.encode('UTF-8')
print("\noriginal msg:", msg_original)
print("\noriginal msg bytes:", msg)

# privKey = secrets.randbelow(curve.field.n)
# pubKey = privKey * curve.g


privKey = 75677893082214022181288368249477912165876056778864066604224293342946349201912
pubKey = privKey * curve.g

print("\nprivKey: ", type(privKey))
print("\npubKey: ", type(pubKey))

encryptedMsg = encrypt_ECC(msg, pubKey)
encryptedMsgObj = {
    'ciphertext': binascii.hexlify(encryptedMsg[0]),
    'nonce': binascii.hexlify(encryptedMsg[1]),
    'authTag': binascii.hexlify(encryptedMsg[2]),
    'ciphertextPubKey': hex(encryptedMsg[3].x) + hex(encryptedMsg[3].y % 2)[2:]
}
print("\npublic key:", pubKey)
print("\nprivKey key:", privKey)
print("\nencrypted msg:", encryptedMsg)
print("\nencrypted msg object:", encryptedMsgObj)

decryptedMsg = decrypt_ECC(encryptedMsg, privKey)
print("\ndecrypted msg bytes:", decryptedMsg)
print("\ndecrypted msg:", decryptedMsg.decode('UTF-8'))
