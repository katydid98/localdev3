# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
#from django.db.models.signals import pre_save
#from .models import Choice, Question
#from .signals import check_user_words
#import Polls.apps.signals

class PollsConfig(AppConfig):
    name = 'polls'

    # def ready(self):
    # 	pre_save.connect(check_user_words, sender=Question)
    # 	pre_save.connect(check_user_words, sender=Choice)
    	

