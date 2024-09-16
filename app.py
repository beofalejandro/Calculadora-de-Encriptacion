from flask import Flask as fk, render_template as rt, request as rq
import string
import random

app = fk(__name__)


@app.route('/')
def index():
    return rt('index.html')


@app.route('/cesar-encription')
def cesar_calculator():
    return rt('cesar-encription.html')


@app.route('/rsa-encryption')
def rsa_calculator():
    return rt('rsa-encryption.html')


@app.route('/vigenere-encryption')
def vigenere_calculator():
    return rt('/vigenere-encryption.html')


@app.route('/vernam-encryption')
def vernam_calculator():
    return rt('/vernam-encryption.html')


# CESAR METHODS
def cifrar_cesar(mensaje, desplazamiento):
    alfabeto_mayusculas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alfabeto_minusculas = "abcdefghijklmnopqrstuvwxyz"

    mensaje_cifrado = ""

    for caracter in mensaje:
        if caracter.isspace():
            mensaje_cifrado += caracter
            continue

        if caracter.isupper():
            indice_original = alfabeto_mayusculas.index(caracter)
            indice_cifrado = (indice_original +
                              desplazamiento) % len(alfabeto_mayusculas)
            mensaje_cifrado += alfabeto_mayusculas[indice_cifrado]
        else:
            indice_original = alfabeto_minusculas.index(caracter)
            indice_cifrado = (indice_original +
                              desplazamiento) % len(alfabeto_minusculas)
            mensaje_cifrado += alfabeto_minusculas[indice_cifrado]

    return mensaje_cifrado


def descifrar_cesar(mensaje_cifrado, desplazamiento):
    alfabeto_mayusculas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alfabeto_minusculas = "abcdefghijklmnopqrstuvwxyz"

    mensaje_descifrado = ""

    for caracter in mensaje_cifrado:
        if caracter.isspace():
            mensaje_descifrado += caracter
            continue

        if caracter.isupper():
            indice_cifrado = alfabeto_mayusculas.index(caracter)
            indice_original = (
                indice_cifrado - desplazamiento) % len(alfabeto_mayusculas)
            mensaje_descifrado += alfabeto_mayusculas[indice_original]
        else:
            indice_cifrado = alfabeto_minusculas.index(caracter)
            indice_original = (
                indice_cifrado - desplazamiento) % len(alfabeto_minusculas)
            mensaje_descifrado += alfabeto_minusculas[indice_original]

    return mensaje_descifrado

# VIGENERE ENCRYPTION


def cifrar_vigenere(mensaje, clave):
    alfabeto_mayusculas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alfabeto_minusculas = "abcdefghijklmnopqrstuvwxyz"

    mensaje_cifrado = ""
    clave_index = 0

    for caracter in mensaje:
        if caracter.isspace():
            mensaje_cifrado += caracter
            continue

        if caracter.isupper():
            indice_original = alfabeto_mayusculas.index(caracter)
            indice_clave = alfabeto_mayusculas.index(
                clave[clave_index % len(clave)])
            indice_cifrado = (indice_original +
                              indice_clave) % len(alfabeto_mayusculas)
            mensaje_cifrado += alfabeto_mayusculas[indice_cifrado]
        else:
            indice_original = alfabeto_minusculas.index(caracter)
            indice_clave = alfabeto_minusculas.index(
                clave[clave_index % len(clave)])
            indice_cifrado = (indice_original +
                              indice_clave) % len(alfabeto_minusculas)
            mensaje_cifrado += alfabeto_minusculas[indice_cifrado]

        clave_index += 1

    return mensaje_cifrado


def descifrar_vigenere(mensaje_cifrado, clave):
    alfabeto_mayusculas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alfabeto_minusculas = "abcdefghijklmnopqrstuvwxyz"

    mensaje_descifrado = ""
    clave_index = 0

    for caracter in mensaje_cifrado:
        if caracter.isspace():
            mensaje_descifrado += caracter
            continue

        if caracter.isupper():
            indice_cifrado = alfabeto_mayusculas.index(caracter)
            indice_clave = alfabeto_mayusculas.index(
                clave[clave_index % len(clave)])
            indice_original = (
                indice_cifrado - indice_clave) % len(alfabeto_mayusculas)
            mensaje_descifrado += alfabeto_mayusculas[indice_original]
        else:
            indice_cifrado = alfabeto_minusculas.index(caracter)
            indice_clave = alfabeto_minusculas.index(
                clave[clave_index % len(clave)])
            indice_original = (
                indice_cifrado - indice_clave) % len(alfabeto_minusculas)
            mensaje_descifrado += alfabeto_minusculas[indice_original]

        clave_index += 1

    return mensaje_descifrado


# VERNAM ENCRIPTION
baudot_code = {
    'A': '00011', 'B': '11001', 'C': '01110', 'D': '01001', 'E': '00001',
    'F': '01101', 'G': '11010', 'H': '10100', 'I': '00110', 'J': '01011',
    'K': '01111', 'L': '10010', 'M': '11100', 'N': '01100', 'O': '11000',
    'P': '10110', 'Q': '10111', 'R': '01010', 'S': '00101', 'T': '10000',
    'U': '00111', 'V': '11110', 'W': '10011', 'X': '11101', 'Y': '10101',
    'Z': '10001', ' ': '00000'
}
baudot_code_inv = {v: k for k, v in baudot_code.items()}
# TRANSLATOR TO BINARY BAUDOT


def text_to_baudot(text):
    """Convierte texto a su representación en código Baudot binario."""
    return ''.join(baudot_code.get(char.upper(), '00000') for char in text)

# TRANSLATION FOR TEXT


def baudot_to_text(binary):
    """Convierte una cadena de bits en código Baudot a texto."""
    chars = [baudot_code_inv.get(binary[i:i+5], '?')
             for i in range(0, len(binary), 5)]
    return ''.join(chars)


def vernam_encrypt(plain_text, key):
    # Convertir texto y clave a código Baudot
    binary_plain = text_to_baudot(plain_text)
    binary_key = text_to_baudot(key)

    # Asegurar que la clave es al menos tan larga como el texto
    if len(binary_key) < len(binary_plain):
        raise ValueError("La clave debe ser al menos tan larga como el texto.")

    # Aplicar XOR para cifrar
    cipher_binary = ''.join(str(int(a) ^ int(b))
                            for a, b in zip(binary_plain, binary_key))
    return cipher_binary


def vernam_decrypt(cipher_text, key):
    # Convertir clave a código Baudot
    binary_key = text_to_baudot(key)

    # Aplicar XOR para descifrar
    plain_binary = ''.join(str(int(a) ^ int(b))
                           for a, b in zip(cipher_text, binary_key))

    # Convertir binario a texto
    return baudot_to_text(plain_binary)

# RSA ENCRYPTION METHODS


def create_mapping():
    alphabet = string.ascii_lowercase
    return {char: idx for idx, char in enumerate(alphabet)}


def text_to_numbers(text, mapping):
    return [mapping[char] for char in text.lower() if char in mapping]


def numbers_to_text(numbers, reverse_mapping):
    return ''.join(reverse_mapping[num] for num in numbers)


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def mod_inverse(e, phi):
    m0, x0, x1 = phi, 0, 1
    while e > 1:
        q = e // phi
        e, phi = phi, e % phi
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1


def generate_rsa_keys(p, q):
    # p = 61
    # q = 53
    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.choice([x for x in range(2, phi) if gcd(x, phi) == 1])

    d = mod_inverse(e, phi)

    return (e, n), (d, n)


def rsa_encrypt(numbers, public_key):
    e, n = public_key
    return [(num ** e) % n for num in numbers]


def rsa_decrypt(encrypted_numbers, private_key):
    d, n = private_key
    return [(num ** d) % n for num in encrypted_numbers]


# CESAR ENCRYPTION METHODS
@app.route('/cesar-encrypt', methods=['POST'])
def cesar_encrypt():
    cesar_mensaje = str(rq.form['message'])
    cesar_desplazamiento = int(rq.form['desplazamiento'])

    # CIFRAR
    # cesar_mensaje_cifrado = cifrar_cesar(cesar_mensaje, cesar_desplazamiento)
    return rt('cesar-encription.html', output_cesar_cifrado=str(cifrar_cesar(cesar_mensaje, cesar_desplazamiento)))


@app.route('/cesar-desencrypt', methods=['POST'])
def cesar_desencrypt():
    cesar_cifrado = str(rq.form['message'])
    cesar_desplazamiento = int(rq.form['desplazamiento'])

    # DESIFRAR
    # cesar_mensaje_descifrado = descifrar_cesar(cesar_cifrado, cesar_desplazamiento)
    return rt('cesar-encription.html', output_cesar_descifrado=str(descifrar_cesar(cesar_cifrado, cesar_desplazamiento)))


# VIGENERE
@app.route('/vigenere-encrypt', methods=['POST'])
def vigenere_encrypt():
    vigenere_mensaje = str(rq.form['message'])
    vigenere_clave = str(rq.form['clave'])

    # CIFRAR
    # vigenere_mensaje_cifrado = cifrar_vigenere(vigenere_mensaje, vigenere_clave)
    return rt('vigenere-encryption.html', output_vigenere_cifrado=str(cifrar_vigenere(vigenere_mensaje, vigenere_clave)))


@app.route('/vigenere-desencrypt', methods=['POST'])
def vigenere_desencrypt():
    vigenere_cifrado = str(rq.form['message'])
    vigenere_clave = str(rq.form['clave'])

    # DESCIFRAR
    # vigenere_mensaje_descifrado = descifrar_vigenere(vigenere_cifrado, vigenere_clave)
    return rt('vigenere-encryption.html', output_vigenere_descifrado=str(descifrar_vigenere(vigenere_cifrado, vigenere_clave)))

# VERNAM ENCRYPTION


@app.route('/vernam-encrypt', methods=['POST'])
def vernam_encryption():
    vernam_mensaje = str(rq.form['message'])
    vernam_clave = rq.form['clave']

    return rt('vernam-encryption.html', output_vernam_cifrado=str(vernam_encrypt(vernam_mensaje, vernam_clave)))


@app.route('/vernam-decrypt', methods=['POST'])
def vernam_decryption():
    vernam_cifrado = str(rq.form['message'])
    vernam_clave = rq.form['clave']

    return rt('vernam-encryption.html', output_vernam_desifrado=str(vernam_decrypt(vernam_cifrado, vernam_clave)))

# RSA Encryption


@app.route('/rsa-encrypt', methods=['POST'])
def rsa_encryption():
    rsa_mensaje = str(rq.form['message'])
    rsa_numero_primo1 = int(rq.form['num1'])
    rsa_numero_primo2 = int(rq.form['num2'])
    mapping = create_mapping()
    reverse_mapping = {v: k for k, v in mapping.items()}

    text_numbers = text_to_numbers(rsa_mensaje, mapping)
    public_key, private_key = generate_rsa_keys(
        rsa_numero_primo1, rsa_numero_primo2)
    encrypted_numbers = rsa_encrypt(text_numbers, public_key)
    decrypted_numbers = rsa_decrypt(encrypted_numbers, private_key)

    return rt('rsa-encryption.html', text_to_number=text_to_numbers(rsa_mensaje, mapping), output_rsa_cifrado=str(rsa_encrypt(text_numbers, public_key)), rsa_decifrado=rsa_decrypt(encrypted_numbers, private_key) ,output_rsa_descifrado=str(numbers_to_text(decrypted_numbers, reverse_mapping)))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
