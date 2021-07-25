from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name must be at least 2 characters long."
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name must be at least 2 characters long. "

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        
        user = User.objects.filter(email=postData['email'])
        if len(user) > 0:
            errors['double'] = "User with email address already exists."

        if len(postData['password']) < 8:
            errors["password"] = "Password must be at least 8 characters long."
        return errors

    def validate_login(self, postData):
        errors={}
        user = User.objects.filter(email=postData['email'])
        if len(postData['email']) == 0:
            errors['email'] = "Email not entered."
        if len(postData['password']) < 8:
            errors['password'] = "Password not entered correctly."
        elif bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()) != True:
            errors['password'] = "Email and password do not match."
        return errors

    def validate_edit(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        
        user = User.objects.filter(email=postData['email'])
        if len(user) > 0:
            errors['double'] = "User with email address already exists."

        if len(postData['password']) < 8:
            errors["password"] = "Password must be at least 8 characters long."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class ItemManager(models.Manager):
    def item_validator(self, postData):
        errors = {}
        if len(postData['item']) < 1:
            errors['item'] = "Item name is required."
        if len(postData['description']) < 5:
            errors['description'] = "Description must be at least 5 characters."
        if len(postData['price']) < 1:
            errors['price'] = "Price must be at least 1 character."
        return errors

class Item(models.Model):
    item = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    uploaded_by = models.ForeignKey(User, related_name = "user_items", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField()
    objects = ItemManager()

class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

class Order(models.Model):
    user = models.ForeignKey(User, related_name="user_order", on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

