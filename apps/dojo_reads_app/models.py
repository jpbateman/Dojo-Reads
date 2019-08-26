from django.db import models
from django.core.validators import validate_email

class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data['first_name'])<2:
            errors["first_name"] = "First name should be at least two letters"
        if len(post_data['last_name'])<2:
            errors["last_name"] = "Last name should be at least two letters"
        try:
            validate_email(post_data["email"])
        except:
            errors["email"] = "Please enter a valid email"
        if len(post_data["password"]) < 2:
            errors["password"] = "Please enter a password!"
        if post_data["password"] != post_data["password2"]:
            errors["confirmation"] = "Your passwords didn't match!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return f"<Show objects: {self.first_name} ({self.id})"

class Book(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

class Review(models.Model):
    review = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    book = models.ForeignKey(Book, related_name="review")
    user = models.ForeignKey(User, related_name="review")

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    books = models.ManyToManyField(Book, related_name="authors")




