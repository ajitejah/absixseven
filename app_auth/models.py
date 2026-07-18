import os
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'

    gender  = models.CharField(max_length=1, choices=Gender.choices, blank=True)
    email   = models.EmailField(unique=True)
    photo   = models.ImageField(upload_to='user/photos/', blank=True, null=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def role(self):
        if hasattr(self, "admin"):
            return "admin"
        if hasattr(self, "teacher"):
            return "teacher"
        if hasattr(self, "student"):
            return "student"
        if hasattr(self, "parent"):
            return "parent"
        return None
    
    def save(self, *args, **kwargs):
        # cek apakah update (bukan create)
        if self.pk:
            old = User.objects.get(pk=self.pk)

            # kalau foto berubah → hapus file lama
            if old.photo and old.photo != self.photo:
                if os.path.isfile(old.photo.path):
                    os.remove(old.photo.path)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # hapus file foto saat user dihapus
        if self.photo and os.path.isfile(self.photo.path):
            os.remove(self.photo.path)

        super().delete(*args, **kwargs)
 

class Admin(models.Model):
    position    = models.CharField(max_length=255)
    user        = models.OneToOneField(User, on_delete=models.CASCADE)

class Teacher(models.Model):
    major       = models.CharField(max_length=255) 
    user        = models.OneToOneField(User, on_delete=models.CASCADE)

class Parent(models.Model):
    position    = models.CharField(max_length=255) 
    user        = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.user.first_name or self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name} - {self.user.email}"
        return self.user.email

class Level(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)  # contoh: fa-solid fa-star

    def __str__(self):
        return self.name 

class Student(models.Model):
    grade   = models.CharField(max_length=255)
    address = models.TextField()
    birth   = models.DateField()
    user    = models.OneToOneField(User, on_delete=models.CASCADE)
    level   = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)
    parent  = models.ForeignKey(Parent, on_delete=models.SET_NULL, null=True, blank=True)


