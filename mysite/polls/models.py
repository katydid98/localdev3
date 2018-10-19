# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from polls.validators import validate_badwords
from django.core.urlresolvers import reverse


def check_user_words(sender, instance, **kwargs):
    for field in instance._meta.get_fields():
        if (isinstance(field, models.CharField) and
                validate_badwords(getattr(instance, field.attname))):
            raise ValidationError("We don't use words like '{}' around here!".format(getattr(instance, field.attname)))


class Question(models.Model):
    question_text = models.CharField(max_length=200, validators=[validate_badwords])
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - timedelta(days=1) <= self.pub_date <= now

    def get_absolute_url(self):
        return reverse('polls:detail', kwargs={'pk': self.pk})


pre_save.connect(check_user_words, sender=Question)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200, validators=[validate_badwords])
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


pre_save.connect(check_user_words, sender=Choice)
