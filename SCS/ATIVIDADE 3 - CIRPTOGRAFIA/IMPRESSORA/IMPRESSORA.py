class Impressora:
    def hex_bytes_to_string(self, b):
        sout = ""
        sBgn = ""
        sMd1 = ""
        sEnd = ""
        sSpc = " " * 48  # 48 espaços

        for i in range(len(b)):
            # A cada linha de 16 bytes hexadecimais faz:
            if i % 16 == 0:
                sBgn += f"{i:04x} "  # Monta a String do início com o índice em hexadecimal

            # Monta a String do meio, contendo os bytes lidos
            sMd1 += f"{b[i]:02x} "  # Bytes em hexadecimal

            # Monta a String do final, contendo os caracteres lidos
            if 32 <= b[i] <= 126:
                sEnd += chr(b[i])  # Caractere ASCII
            else:
                sEnd += "."  # Não imprimível

            # Monta linha a cada 16 caracteres lidos
            if (i % 16 == 15) or (i == len(b) - 1):
                # Ajusta os espaços para a linha
                sout += f"{sBgn}{sMd1}{sSpc[(3 * ((i % 16) + 1)):]} - {sEnd}\n"
                sBgn = sMd1 = sEnd = ""

        return sout.strip()  # Remove a última nova linha, se houver