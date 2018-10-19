from django.core.exceptions import ValidationError
from polls.utils import yaml_loader
from string import maketrans
import string


filepath = "polls/static/polls/blacklist.yaml"
config = yaml_loader(filepath)
blacklist = [word.lower() for word in config['blacklist']]


def validate_badwords(value):
    """ remove punctuation from text
        and make it case-insensitive"""
    invalid_words = []
    user_typ = value.encode()
    translate_table = maketrans(string.punctuation, 32 * " ")
    words = user_typ.translate(translate_table).lower().split()
    for bad_word in blacklist:
        for word in words:
            if word == bad_word:
                invalid_words.append(word)
    if len(invalid_words) != 0:
    	raise ValidationError("We don't use words like '{}' around here!!".format(invalid_words))