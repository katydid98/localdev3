# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db.models.signals import pre_save
from polls.validators import validate_badwords


class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default=None, null=True)
    B2B = "B2B"
    B2A = "B2A"
    B2C = "B2C"

    BUSINESS_CHOICES = ((B2B, "B2B"), (B2A, "B2A"), (B2C, "B2C"))
    business = models.CharField(max_length=3,
                                choices=BUSINESS_CHOICES,
                                default=B2A)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


def check_user_words(sender, instance, **kwargs):
    for field in instance._meta.get_fields():
        if (isinstance(field, models.CharField)):
                validate_badwords(getattr(instance, field.attname))


class Question(models.Model):
    question_text = models.CharField(max_length=200,
                                     validators=[validate_badwords])
    pub_date = models.DateTimeField('date published')
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                null=True,
                                default=None)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200,
                                   validators=[validate_badwords])
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


pre_save.connect(check_user_words, sender=Question)
pre_save.connect(check_user_words, sender=Choice)
