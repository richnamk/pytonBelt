from __future__ import unicode_literals
from django.db import models
import bcrypt

class UserManager(models.Manager):
    def validate_registration(self, form_data):
        errors =[]

        if len(form_data['name']) == 0:
            errors.append("name is needed.")

        if len(form_data['alias']) == 0:
            errors.append("alias is needed.")
      
        if len(form_data['email']) == 0:
            errors.append("email is needed.")
      
        if len(form_data['password']) == 0:
            errors.append("password is needed.")
       
        if form_data['password'] != form_data['password_confirmation']:
            errors.append("passwords dont match.")

        return errors

    def validate_login(self, form_data):
        errors = []
       
        if len(form_data['email']) == 0:
            errors.append("email is needed.")
       
        if len(form_data['password']) == 0:
            errors.append("password is needed.")

        user = User.objects.filter(email=form_data['email']).first()

        if user:
            user_password = form_data['password'].encode()
            db_password = user.password.encode()

            if bcrypt.checkpw(user_password, db_password):
                return {'user': user}

            errors.append("Invalid password")
        errors.append("Invalid account")

        return {'errors': errors}

    def create_user(self, form_data):
        hashedpw = bcrypt.hashpw(form_data['password'].encode(), bcrypt.gensalt())

        return User.objects.create(
            name = form_data['name'],
            alias = form_data['alias'],
            email = form_data['email'],
            password = hashedpw,
    )

class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
