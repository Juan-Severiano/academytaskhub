from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name


class Discipline(models.Model):
    name = models.CharField(max_length=20)
    is_technical_area = models.BooleanField()

    def __str__ (self) -> str:
        return self.name


class ItemList(models.Model):
    STATUS = (
        ('TODO', 'To Do'),
        ('DOING', 'Doing'),
        ('DONE', 'Done'),
    )

    TYPE = (
        ('P', 'Pessoal'),
        ('A', 'Para todos')
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=150)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField()
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, blank=True, null=True)
    teacher = models.ForeignKey(Teacher, models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=5, choices=STATUS)
    type = models.CharField(max_length=1, choices=TYPE)
    root = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title


class Person(models.Model):
    LEVEL = (
        ('AD', 'Admin'),
        ('PR', 'Professor'),
        ('AL', 'Aluno')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=2, choices=LEVEL)
    item_list = models.ManyToManyField(ItemList, blank=True)

    def __str__(self):
        return self.user.username