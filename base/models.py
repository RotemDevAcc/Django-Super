from django.db import models

# Create your models here.

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    def __str__(self):
        return self.description

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    price = models.FloatField()
    img = models.ImageField(null=True,blank=True,default='/placeholder.png')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Foreign key to Category
    def __str__(self):
        return self.description
    
