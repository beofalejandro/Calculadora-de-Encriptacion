# Tabla de código Baudot simplificada (5 bits por carácter)
baudot_code = {
    'A': '00011', 'B': '11001', 'C': '01110', 'D': '01001', 'E': '00001',
    'F': '01101', 'G': '11010', 'H': '10100', 'I': '00110', 'J': '01011',
    'K': '01111', 'L': '10010', 'M': '11100', 'N': '01100', 'O': '11000',
    'P': '10110', 'Q': '10111', 'R': '01010', 'S': '00101', 'T': '10000',
    'U': '00111', 'V': '11110', 'W': '10011', 'X': '11101', 'Y': '10101',
    'Z': '10001', ' ': '00000'  # Incluimos el espacio como parte del mapeo
}

# Inversa para descifrar
baudot_code_inv = {v: k for k, v in baudot_code.items()}

def text_to_baudot(text):
    """Convierte texto a su representación en código Baudot binario."""
    return ''.join(baudot_code.get(char.upper(), '00000') for char in text)

def baudot_to_text(binary):
    """Convierte una cadena de bits en código Baudot a texto."""
    chars = [baudot_code_inv.get(binary[i:i+5], '?') for i in range(0, len(binary), 5)]
    return ''.join(chars)

def vernam_encrypt(plain_text, key):
    """Cifra el texto plano usando el cifrado Vernam."""
    # Convertir texto y clave a código Baudot
    binary_plain = text_to_baudot(plain_text)
    binary_key = text_to_baudot(key)
    
    # Asegurar que la clave es al menos tan larga como el texto
    if len(binary_key) < len(binary_plain):
        raise ValueError("La clave debe ser al menos tan larga como el texto.")

    # Aplicar XOR para cifrar
    cipher_binary = ''.join(str(int(a) ^ int(b)) for a, b in zip(binary_plain, binary_key))
    return cipher_binary

def vernam_decrypt(cipher_text, key):
    """Descifra el texto cifrado usando el cifrado Vernam."""
    # Convertir clave a código Baudot
    binary_key = text_to_baudot(key)
    
    # Aplicar XOR para descifrar
    plain_binary = ''.join(str(int(a) ^ int(b)) for a, b in zip(cipher_text, binary_key))
    
    # Convertir binario a texto
    return baudot_to_text(plain_binary)

# Ejemplo de uso
mensaje = "HELLO WOLRD"
clave = "10001 10001 11000"

# Cifrar
cifrado = vernam_encrypt(mensaje, clave)
print(f"Texto cifrado: {cifrado}")

# Descifrar
descifrado = vernam_decrypt(cifrado, clave)
print(f"Texto descifrado: {descifrado}")
