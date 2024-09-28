import os
import pickle
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes


class CryptoRSA:
    def __init__(self):
        self.texto_cifrado = None
        self.texto_decifrado = None

    def gera_par_de_chaves(self, f_pub, f_prv):
        # Gera um par de chaves RSA
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=1024,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        # Gravando a chave pública em formato serializado
        with open(f_pub, 'wb') as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

        # Gravando a chave privada em formato serializado
        with open(f_prv, 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

    def gera_cifra(self, texto, f_pub):
        # Lê a chave pública do arquivo
        with open(f_pub, 'rb') as f:
            public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())

        # Cifra o texto
        self.texto_cifrado = public_key.encrypt(
            texto,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def get_texto_cifrado(self):
        return self.texto_cifrado

    def gera_decifra(self, texto, f_prv):
        # Lê a chave privada do arquivo
        with open(f_prv, 'rb') as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())

        # Decifra o texto
        self.texto_decifrado = private_key.decrypt(
            texto,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def get_texto_decifrado(self):
        return self.texto_decifrado


# Exemplo de uso
if __name__ == "__main__":
    crypto = CryptoRSA()

    # Gerar chaves e salvar em arquivos
    crypto.gera_par_de_chaves('chave_pub.pem', 'chave_prv.pem')

    # Texto a ser cifrado
    texto = b"Mensagem Secreta"

    # Cifrar o texto
    crypto.gera_cifra(texto, 'chave_pub.pem')
    texto_cifrado = crypto.get_texto_cifrado()
    print("Texto Cifrado:", texto_cifrado)

    # Decifrar o texto
    crypto.gera_decifra(texto_cifrado, 'chave_prv.pem')
    texto_decifrado = crypto.get_texto_decifrado()
    print("Texto Decifrado:", texto_decifrado.decode())

