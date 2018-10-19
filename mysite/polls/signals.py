# from .models import contains_bad_words
# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from django.core.exceptions import ValidationError
# from django.db import models


# #@receiver(pre_save)
# def check_user_words(sender, instance, **kwargs):
#     for field in instance._meta.get_fields():
#         if (isinstance(field, models.CharField) and
#                 contains_bad_words(getattr(instance, field.attname))):
#             raise ValidationError("We don't use words like '{}' around here!".format(getattr(instance, field.attname))) 