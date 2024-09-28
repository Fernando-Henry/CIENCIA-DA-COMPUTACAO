import random
import pickle


class CryptoDummy:
    def __init__(self):
        self.texto_cifrado = None
        self.texto_decifrado = None

    def gera_chave(self, f_dummy):
        # Gera uma chave Dummy simétrica (dk: 0 a 100)
        dk = int(random.random() * 101)  # Equivalente ao Math.random() * 101
        # Grava a chave Dummy em formato serializado
        with open(f_dummy, 'wb') as f:
            pickle.dump(dk, f)

    def gera_cifra(self, texto, f_dummy):
        # Lê a chave Dummy do arquivo serializado
        with open(f_dummy, 'rb') as f:
            i_dummy = pickle.load(f)

        self.texto_cifrado = texto
        # Aplica a cifra
        for i in range(len(self.texto_cifrado)):
            self.texto_cifrado[i] = (self.texto_cifrado[i] + i + i_dummy)

    def get_texto_cifrado(self):
        return self.texto_cifrado

    def gera_decifra(self, texto, f_dummy):
        # Lê a chave Dummy do arquivo serializado
        with open(f_dummy, 'rb') as f:
            i_dummy = pickle.load(f)

        self.texto_decifrado = texto
        # Aplica a decifração
        for i in range(len(self.texto_decifrado)):
            self.texto_decifrado[i] = (self.texto_decifrado[i] - i - i_dummy)

    def get_texto_decifrado(self):
        return self.texto_decifrado


# Exemplo de uso:
crypto = CryptoDummy()
texto_original = bytearray(b"Mensagem Secreta!")  # byte[] equivalente em Python
arquivo_chave = "chave_dummy.dat"

# Gerar a chave
crypto.gera_chave(arquivo_chave)

# Cifrar o texto
crypto.gera_cifra(texto_original, arquivo_chave)
print("Texto Cifrado:", crypto.get_texto_cifrado())

# Decifrar o texto
crypto.gera_decifra(crypto.get_texto_cifrado(), arquivo_chave)
print("Texto Decifrado:", crypto.get_texto_decifrado().decode())  # Decodifica os bytes para string
