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

# class ProductReview(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_review")
#     product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="product_review")
#     comments = models.TextField()
#     ratings = models.DecimalField(max_digits=6,decimal_places=1)
    
#     class Meta:
#         unique_together = ("user", "product")



# Create your models here.
class ProductReview(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    product= models.ForeignKey(Product,related_name='review',on_delete=models.CASCADE)
    comments = models.TextField()
    reviewed_date= models.DateTimeField(auto_now_add=True)
    ratings = models.DecimalField(max_digits=6,decimal_places=1)
    
    reply= models.ForeignKey('self', on_delete=models.CASCADE,null=True, blank=True, related_name='replies')
    

    def __str__(self):
        return f"{self.user.first_name} - {self.comments[:20]}"
    class Meta:
         unique_together = ("user", "product")
    
class ReviewImage(models.Model):
    review=models.ForeignKey(ProductReview, related_name='review_image',on_delete=models.CASCADE)
    review_image = models.ImageField(upload_to='review_uploads/',blank=True,null=True)
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.review.comments[:10]} by {self.review.user}"