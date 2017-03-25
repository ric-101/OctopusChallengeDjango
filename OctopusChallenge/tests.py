# -*- coding: utf-8 -*-

from django.test import TestCase

from tools import *


class TestCryptography(TestCase):

    def setUp(self):
        self.words = ["dog", "dog's", "pharmacy", "cioè"]
        self.keys = [
            Random.new().read(16),
            Random.new().read(16),
            Random.new().read(32),
        ]

    def test_hashing(self):
        for word in self.words:
            self.assertEqual(get_hash(word), get_hash(word))
            self.assertNotEqual(get_hash(word), get_hash(word, 'salt'))
            self.assertNotEqual(get_hash(word, 'pepper'), get_hash(word, 'salt'))

    def test_encryption(self):
        for word in self.words:
            print('testing word: {0}'.format(word))
            self.assertEqual(word, decrypt(encrypt(word, self.keys[0]), self.keys[0]))
            self.assertEqual(word, encrypt(word, self.keys[0]))
            self.assertEqual(word, encrypt(word, ''))
            self.assertNotEqual(word, encrypt(word, '').split('#####')[0])
            self.assertNotEqual(word, encrypt(word, '').split('#####')[1])
            self.assertNotEqual(encrypt(word, self.keys[0]), encrypt(word, self.keys[0]))
            self.assertNotEqual(encrypt(word, self.keys[0]), encrypt(word, ''))
            self.assertNotEqual(encrypt(word, self.keys[0]), encrypt(word, self.keys[1]))
            self.assertNotEqual(encrypt(word, self.keys[0]), encrypt(word, self.keys[2]))
            self.assertNotEqual(word, decrypt(encrypt(word, self.keys[0]), self.keys[1]))
            self.assertNotEqual(word, decrypt(encrypt(word, self.keys[0]), self.keys[2]))
            self.assertNotEqual(word, decrypt(encrypt(word, ''), self.keys[2]))
            self.assertNotEqual(word, decrypt(encrypt(word, self.keys[0]), ''))

    def test_database(self):
        pass
