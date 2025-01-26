from django.contrib.auth.models import AbstractUser
from django.db import models

# Định nghĩa User kế thừa từ AbstractUser
class User(AbstractUser):
    pass  # Thêm các trường tùy chỉnh nếu cần

    def __str__(self):
        return self.username

# Định nghĩa Pet
class Pet(models.Model):
    name = models.CharField(max_length=255)
    species = models.CharField(max_length=255)
    age = models.IntegerField()
    sex = models.CharField(max_length=50)
    health = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)  # Ngày sinh
    description = models.TextField(null=True, blank=True)  # Mô tả chi tiết
    is_available_for_adoption = models.BooleanField(default=True)  # Trạng thái nhận nuôi

    def __str__(self):
        return f"{self.name} ({self.species}) - Owner: {self.owner.username if self.owner else 'No owner'}"
