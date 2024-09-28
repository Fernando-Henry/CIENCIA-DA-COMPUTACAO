from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os
import pickle


class CryptoAES:
    def __init__(self):
        self.texto_cifrado = None
        self.texto_decifrado = None

    def gera_chave(self, f_sim):
        # Gera uma chave simétrica de 128 bits
        chave = get_random_bytes(16)  # 16 bytes = 128 bits
        with open(f_sim, 'wb') as file:
            pickle.dump(chave, file)

    def gera_cifra(self, texto, f_sim):
        with open(f_sim, 'rb') as file:
            chave = pickle.load(file)

        # Cifra o texto
        iv = get_random_bytes(AES.block_size)  # Gera um IV aleatório
        cipher = AES.new(chave, AES.MODE_CBC, iv)
        self.texto_cifrado = iv + cipher.encrypt(self._pad(texto))

    def get_texto_cifrado(self):
        return self.texto_cifrado

    def gera_decifra(self, texto, f_sim):
        with open(f_sim, 'rb') as file:
            chave = pickle.load(file)

        # Decifra o texto
        iv = texto[:AES.block_size]  # Extrai o IV
        cipher = AES.new(chave, AES.MODE_CBC, iv)
        self.texto_decifrado = self._unpad(cipher.decrypt(texto[AES.block_size:]))

    def get_texto_decifrado(self):
        return self.texto_decifrado

    @staticmethod
    def _pad(data):
        # Adiciona padding ao texto para que seu tamanho seja múltiplo do bloco
        pad_len = AES.block_size - len(data) % AES.block_size
        return data + bytes([pad_len] * pad_len)

    @staticmethod
    def _unpad(data):
        # Remove o padding do texto
        pad_len = data[-1]
        return data[:-pad_len]


# Exemplo de uso:
if __name__ == "__main__":
    crypto = CryptoAES()

    # Gerar chave e salvar em um arquivo
    crypto.gera_chave('chave_sim.pkl')

    # Texto a ser cifrado
    texto = b"TestandoUma$enha123"

    # Cifrar o texto
    crypto.gera_cifra(texto, 'chave_sim.pkl')
    texto_cifrado = crypto.get_texto_cifrado()
    print("Texto Cifrado:", texto_cifrado)

    # Decifrar o texto
    crypto.gera_decifra(texto_cifrado, 'chave_sim.pkl')
    texto_decifrado = crypto.get_texto_decifrado()
    print("Texto Decifrado:", texto_decifrado.decode())

