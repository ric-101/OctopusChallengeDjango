import os
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import requests
from bs4 import BeautifulSoup
from django.conf import settings


def get_url_text(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url

    try:
        url_html = requests.get(url).content
    except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL):
        return None

    # url_text = BeautifulSoup(url_html, 'html.parser').get_text()
    soup = BeautifulSoup(url_html)
    [s.extract() for s in soup(['style', 'script'])]
    url_text = soup.getText()
    return url_text


class LanguageParser:
    __parsers = {}

    class __LanguageParser:
        def __init__(self, language):
            self.language = language
            self.all_words = set()

            if language is not None:
                language_path = os.path.join(settings.BASE_DIR,
                                             'OctopusChallenge',
                                             'resources', 'languages', language)
                language_files = [f for f in os.listdir(language_path)]
            else:
                language_files = []

                # one set of words for each file in the language's folder,
            # for each file, creates an attribute with the same name as the file
            for language_file in language_files:
                with open(os.path.join(language_path, language_file)) as fp:
                    words = fp.readlines()
                    words = [word.strip() for word in words]
                    setattr(self, language_file, set(words))

        def count_words(self, text, words_types):
            """
            :param text: text to parse
            :param words_types: list ot tuple of strings, ie:  ['nouns', 'verbs']
            :return:
            """

            def add_word(word, parsed_words):
                try:
                    parsed_words[word] += 1
                except KeyError:
                    parsed_words[word] = 1

            parsed_words = {}

            # select and count all words (of allowed type)
            if self.language is None:
                for word in text.split():
                    if self.language is None:
                        add_word(word, parsed_words)

            else:
                for word_type in words_types:
                    if not hasattr(self, word_type):
                        raise Exception(
                            'Error: missing dictionary of {0}'.format(word_type))

                for word in text.split():
                    for words_type in words_types:
                        if word in getattr(self, words_type):
                            add_word(word, parsed_words)
                            break

            return parsed_words

        @staticmethod
        def prepare_word_for_server(word, freq):
            try:
                return {
                    'id': Crypto.hash(word, settings.CRYPTO['salt']),
                    '_word': Crypto.encrypt(word, settings.CRYPTO['key']),
                    'word': word,
                    'freq': freq,
                }
            except:
                # some words be invalid for hashing or encryption
                return None

        def get_words_list(self, words_dict):
            words = []
            for word_dict in words_dict:
                word = self.prepare_word_for_server(word_dict, words_dict[word_dict])
                if word is None:
                    print('Warning! invalid word')
                else:
                    words.append(word)

            words.sort(key=lambda k: k['freq'], reverse=True)
            return words[:settings.MAX_WORDS_PER_URL]


    @classmethod
    def __get_parser(cls, language):
        try:
            return cls.__parsers[language]
        except KeyError:
            parser = cls.__LanguageParser(language)
            cls.__parsers[language] = parser
            return parser

    @classmethod
    def parse(cls, text, words_types=('all', ), language=None):
        if language is None:
            if 'all' not in words_types:
                raise Exception("Words_types must be 'all' if no language is selected")

        parser = cls.__get_parser(language)
        words_dict = parser.count_words(text, words_types)
        words_list = parser.get_words_list(words_dict)
        return words_list


class Crypto:
    __ciphers = {}

    class __AESCipher:
        def __init__(self, key):
            self.bs = 32
            self.key = hashlib.sha256(key.encode()).digest()

        def encrypt(self, raw):
            raw = self._pad(raw)
            iv = Random.new().read(AES.block_size)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return base64.b64encode(iv + cipher.encrypt(raw))

        def decrypt(self, enc):
            enc = base64.b64decode(enc)
            iv = enc[:AES.block_size]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

        def _pad(self, s):
            return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

        @staticmethod
        def _unpad(s):
            return s[:-ord(s[len(s)-1:])]

    @classmethod
    def __get_cypher(cls, key):
        try:
            return cls.__ciphers[key]
        except KeyError:
            cipher = cls.__AESCipher(key)
            cls.__ciphers[key] = cipher
            return cipher

    @classmethod
    def encrypt(cls, txt, key):
        cipher = cls.__get_cypher(key)
        return cipher.encrypt(txt)

    @classmethod
    def decrypt(cls, encripted_txt, key):
        cipher = cls.__get_cypher(key)
        return cipher.decrypt(encripted_txt)

    @staticmethod
    def hash(txt, salt=None):
        hasher = SHA256.new()
        hasher.update(txt)
        if salt is not None:
            hasher.update(salt)

        return hasher.hexdigest()
