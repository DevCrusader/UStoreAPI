from hashlib import sha256
from django.db import models


class SecretWord(models.Model):
    """
    Model contains information about current secret word
    to access to service.
    Using hashlib.sha256.

    It includes:
        word:       required string field with max_length = 250,
                    contains encoded word.
        created_date:
                    datetime field.
    """
    word = models.CharField(max_length=250, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Секретное слово"
        verbose_name_plural = "Секретные слова"
        ordering = ["-created_date"]

    def check_secret_word(self, word):
        """
        Checks the requested secret word
        """
        return sha256(word.encode()).hexdigest() == self.word

    def save(self, *args, **kwargs):
        self.word = sha256(self.word.encode()).hexdigest()
        super(SecretWord, self).save(*args, **kwargs)
