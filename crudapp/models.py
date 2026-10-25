from django.db import models

# Student Model.
class Student(models.Model):
    name = models.CharField(max_length=50,null=False)
    age = models.PositiveIntegerField(null=False)
    email= models.EmailField(max_length=50,unique=True,null=False)

    def __str__(self):
        return f"Name : {self.name} | Age : {self.age} | Email : {self.email}"