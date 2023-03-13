from django.db import models
from datetime import datetime
# Create your models here.


class UserModel(models.Model):
	PhoneNumber= models.IntegerField(max_length = 100 , blank = True)
	Email = models.EmailField(max_length = 100 , blank = True)
	Is_customer = models.BooleanField()
	Is_admin=models.BooleanField()
class UserProfileModel(models.Model):
	owner=models.OneToOneField()
	 Name = models.CharField(max_length = 100 , blank = True)
	 dateofbirth=models.DateTimeField()
	 Image=models.ImageField(upload_to="/images")
class ProductMainModel(models.Model):
	Title=models.CharField(max_length=100)
	description=models.TextField()
	Unique_Id=models.IntegerField()
	Price=models.IntegerField()

