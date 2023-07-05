from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    product_id=models.AutoField
    product_name=models.CharField(max_length=50)
    price=models.IntegerField(default=0)
    category=models.CharField(max_length=50,default="")
    subcategory=models.CharField(max_length=50,default="")
    image=models.ImageField(upload_to="craft/images",default="")
    
    def __str__(self):
        return self.product_name
    
class Orders(models.Model):
    order_id=models.AutoField(primary_key=True)
    items_json=models.CharField(max_length=120)
    amount=models.IntegerField(default=0)
    name=models.CharField(max_length=122)
    email=models.CharField(max_length=122,default="")
    address=models.CharField(max_length=122,default="")
    city=models.CharField(max_length=1000,default="")
    state=models.CharField(max_length=1000,default="")
    zip_code=models.CharField(max_length=1000,default="")
    phone=models.CharField(max_length=122,default="")
    

    
    







