from __future__ import unicode_literals

from django.conf import settings
from django.db import models
import tools


class Word(models.Model):
    word_salt = settings.CRYPTO['salt']
    crypto_key = settings.CRYPTO['key']

    # word's salted hash
    id = models.CharField(max_length=255, primary_key=True, unique=True, null=False)

    # encrypted word (used for @property)
    _word = models.CharField(max_length=1024, unique=True, null=False)

    # total number of times this word has appeared
    freq = models.IntegerField(null=False, default=0)

    @property
    def word(self):
        return tools.Crypto.decrypt(self._word, self.crypto_key)

    @classmethod
    def add_word(cls, word_dict):
        """
        :param word: dict as created by __LanguageParser.prepare_word()
        """
        try:
            word = cls.objects.get(id=word_dict['id'])
            word.freq += word_dict['freq']
        except cls.DoesNotExist:
            word = cls(
                id=word_dict['id'],
                _word=word_dict['_word'],
                freq=word_dict['freq']
            )

        word.save()
        return word
