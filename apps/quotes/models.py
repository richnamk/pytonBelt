from __future__ import unicode_literals
from ..login.models import User
from django.db import models

class QuoteManager(models.Manager):

    def validate(self, form_data):
        errors = []

        if len(form_data['quoted_by']) < 3:
            errors.append("Quoted by must be more than 3 char")

        if len(form_data['message']) < 10:
            errors.append("Type more than 10 char for the message")
    
        return errors

    def create_quote(self, form_data, user_id):

        quoted_by = form_data['quoted_by']
        message = form_data['message']

        user = User.objects.get(id=user_id)

        posted_by = user

        self.create(message=message, quoted_by=quoted_by, posted_by=user)

class Quote(models.Model):

    quoted_by = models.CharField(max_length=150)
    message = models.CharField(max_length=150)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    posted_by = models.ForeignKey(User, related_name="posted_quotes")

    favorited_by = models.ManyToManyField(User, related_name="favorites")

    objects = QuoteManager()

    def __str__(self):
        return "{} {} {}".format(self.quoted_by, self.message, self.posted_by)
