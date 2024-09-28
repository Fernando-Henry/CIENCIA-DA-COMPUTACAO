from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import os

class Impressora:
    @staticmethod
    def hex_bytes_to_string(b):
        return ''.join(f'{byte:02x}' for byte in b)

class CryptoAES:
    def __init__(self):
        self.key = None
        self.cipher = None

    def gera_chave(self):
        self.key = get_random_bytes(16)  # Chave de 128 bits

    def gera_cifra(self, msg):
        self.cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = self.cipher.encrypt(pad(msg, AES.block_size))
        return self.cipher.iv + ct_bytes  # Retorna IV + ciphertext

    def gera_decifra(self, ciphertext):
        iv = ciphertext[:16]
        ct = ciphertext[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), AES.block_size)

class CryptoRSA:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def gera_par_de_chaves(self):
        key = RSA.generate(2048)
        self.private_key = key.export_key()
        self.public_key = key.publickey().export_key()

    def gera_cifra(self, msg):
        cipher = PKCS1_OAEP.new(RSA.import_key(self.public_key))
        return cipher.encrypt(msg)

    def gera_decifra(self, ciphertext):
        cipher = PKCS1_OAEP.new(RSA.import_key(self.private_key))
        return cipher.decrypt(ciphertext)

def main():
    from base64 import b64encode  # Importando b64encode aqui
    s_msg_clara = "Oi, alunos do IMT!"
    b_msg_clara = s_msg_clara.encode("ISO-8859-1")

    # Impressão da mensagem original
    prn = Impressora()
    print("---")
    print(">>> Imprimindo mensagem original...")
    print("")
    print("Mensagem Clara (Hexadecimal):")
    print(prn.hex_bytes_to_string(b_msg_clara))
    print("Mensagem Clara (String):")
    print(s_msg_clara)
    print("")

    # Criptografia AES
    print(">>> Cifrando com o algoritmo AES...")
    print("")
    caes = CryptoAES()
    caes.gera_chave()
    b_msg_cifrada = caes.gera_cifra(b_msg_clara)

    print("Mensagem Cifrada (Hexadecimal):")
    print(prn.hex_bytes_to_string(b_msg_cifrada))
    print("Mensagem Cifrada (String):")
    print(b64encode(b_msg_cifrada).decode('ISO-8859-1'))
    print("")

    print(">>> Decifrando com o algoritmo AES...")
    print("")
    b_msg_decifrada = caes.gera_decifra(b_msg_cifrada)

    print("Mensagem Decifrada (Hexadecimal):")
    print(prn.hex_bytes_to_string(b_msg_decifrada))
    print("Mensagem Decifrada (String):")
    print(b_msg_decifrada.decode("ISO-8859-1"))
    print("")

    # Criptografia RSA
    print(">>> Cifrando com o algoritmo RSA...")
    print("")
    crsa = CryptoRSA()
    crsa.gera_par_de_chaves()
    b_msg_cifrada_rsa = crsa.gera_cifra(b_msg_clara)

    print("Mensagem Cifrada (Hexadecimal):")
    print(prn.hex_bytes_to_string(b_msg_cifrada_rsa))
    print("Mensagem Cifrada (String):")
    print(b64encode(b_msg_cifrada_rsa).decode('ISO-8859-1'))
    print("")

    print(">>> Decifrando com o algoritmo RSA...")
    print("")
    b_msg_decifrada_rsa = crsa.gera_decifra(b_msg_cifrada_rsa)

    print("Mensagem Decifrada (Hexadecimal):")
    print(prn.hex_bytes_to_string(b_msg_decifrada_rsa))
    print("Mensagem Decifrada (String):")
    print(b_msg_decifrada_rsa.decode("ISO-8859-1"))
    print("")

if __name__ == "__main__":
    main()
