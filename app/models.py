from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    name = models.CharField(max_length=20)

    def __str__ (self) -> str:
        return self.name


class Discipline(models.Model):
    name = models.CharField(max_length=20)
    is_technical_area = models.BooleanField()

    def __str__ (self) -> str:
        return self.name
    

class ItemList(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=150)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    due_date = models.DateField()
    discipline = models.ForeignKey(
        Discipline, on_delete=models.CASCADE
    )
    teacher = models.ForeignKey(
        Teacher, models.CASCADE
    )

    def __str__(self) -> str:
        return self.title
