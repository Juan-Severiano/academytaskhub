from unittest import TestCase
from utils import token_generate


class TokenGenerateTest(TestCase):
    def test_vigenere_decrypt(self):
        key = 'batatafrita123'
        email = 'emaildabata@gmail.com'

        encrypt = token_generate.vigenere_encrypt(email, key)
        decrypt = token_generate.vigenere_decrypt(encrypt, key)

        self.assertEqual(email, decrypt)
