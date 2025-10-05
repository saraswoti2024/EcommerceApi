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
    price = models.DecimalField(max_digits=10,decimal_places = 3)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)    
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE) 
    rating = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.name}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products_images')
    videos = models.FileField(upload_to='products_videos',blank=True,null=True)
    color = models.CharField(max_length=20,default="black")

    def __str__(self):
        return f"{self.product.name} - img/vid"



class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("user", "product")

class WishlistItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="wishlist_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "product")