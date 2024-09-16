import string
import random

# Crear el mapeo entre letras y números
def create_mapping():
    alphabet = string.ascii_lowercase
    return {char: idx for idx, char in enumerate(alphabet)}

# Convertir texto a números
def text_to_numbers(text, mapping):
    return [mapping[char] for char in text.lower() if char in mapping]

# Convertir números a texto
def numbers_to_text(numbers, reverse_mapping):
    return ''.join(reverse_mapping[num] for num in numbers)

# Función para calcular el máximo común divisor
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Función para calcular el inverso modular usando el algoritmo extendido de Euclides
def mod_inverse(e, phi):
    m0, x0, x1 = phi, 0, 1
    while e > 1:
        q = e // phi
        e, phi = phi, e % phi
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

# Función para generar claves RSA
def generate_rsa_keys():
    # Dos números primos grandes (puedes cambiarlos por valores más grandes)
    p = 61
    q = 53
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Elegir un entero 'e' tal que 1 < e < phi y gcd(e, phi) = 1
    e = random.choice([x for x in range(2, phi) if gcd(x, phi) == 1])
    
    # Calcular d, el inverso modular de e
    d = mod_inverse(e, phi)
    
    # Clave pública (e, n) y clave privada (d, n)
    return (e, n), (d, n)

# Cifrar usando la clave pública
def rsa_encrypt(numbers, public_key):
    e, n = public_key
    return [(num ** e) % n for num in numbers]

# Descifrar usando la clave privada
def rsa_decrypt(encrypted_numbers, private_key):
    d, n = private_key
    return [(num ** d) % n for num in encrypted_numbers]

def main():
    # Crear el mapeo entre letras y números
    mapping = create_mapping()
    reverse_mapping = {v: k for k, v in mapping.items()}
    
    # Texto a cifrar
    text = "rojo"
    
    # Convertir el texto en números
    text_numbers = text_to_numbers(text, mapping)
    print(f"Texto convertido a números: {text_numbers}")
    
    # Generar claves RSA
    public_key, private_key = generate_rsa_keys()
    print(f"Clave pública: {public_key}")
    print(f"Clave privada: {private_key}")
    
    # Cifrar los números usando la clave pública
    encrypted_numbers = rsa_encrypt(text_numbers, public_key)
    print(f"Números cifrados con RSA: {encrypted_numbers}")
    
    # Descifrar los números usando la clave privada
    decrypted_numbers = rsa_decrypt(encrypted_numbers, private_key)
    print(f"Números descifrados: {decrypted_numbers}")
    
    # Convertir los números descifrados de vuelta a texto
    decrypted_text = numbers_to_text(decrypted_numbers, reverse_mapping)
    print(f"Texto descifrado: {decrypted_text}")

if __name__ == "__main__":
    main()