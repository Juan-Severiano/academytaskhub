def vigenere_encrypt(plaintext, key):
    encrypted_text = ""
    key_len = len(key)
    for i, char in enumerate(plaintext):
        shift = ord(key[i % key_len]) - ord('a')
        if char.isalpha():
            base = ord('a') if char.islower() else ord('A')
            encrypted_char = chr((ord(char) - base + shift) % 26 + base)
        else:
            encrypted_char = char
        encrypted_text += encrypted_char
    return encrypted_text


def vigenere_decrypt(ciphertext, key):
    decrypted_text = ""
    key_len = len(key)
    for i, char in enumerate(ciphertext):
        shift = ord(key[i % key_len]) - ord('a')
        if char.isalpha():
            base = ord('a') if char.islower() else ord('A')
            decrypted_char = chr((ord(char) - base - shift) % 26 + base)
        else:
            decrypted_char = char
        decrypted_text += decrypted_char
    return decrypted_text
