from django.db import models
from accounts.models import CustomUser

class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.category_name}"

class Brand(models.Model):
    Brand_name = models.CharField(max_length=50)
    def __str__(self):
    
        return f"{self.Brand_name}"

class Product(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10,decimal_places = 3)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)    
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE) 
    
    def __str__(self):
        return f"{self.name}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products_images')
    videos = models.FileField(upload_to='products_videos',blank=True,null=True)

    def __str__(self):
        return f"{self.product.name} - img/vid"


class UserChoice(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="user_choice") 
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_choice")
    is_wishlist = models.BooleanField(default=False)
    is_fav = models.BooleanField(default=False)
    add_to_cart = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} - {self.product.name}"
