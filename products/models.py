from django.db import models
from accounts.models import CustomUser
from datetime import datetime

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
    stocks = models.IntegerField(default=0)
    
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

    # class Meta:
    #     unique_together = ("user", "product")

class WishlistItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="wishlist_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "product")

class ProductReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_review")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="product_review")
    comments = models.TextField()
    ratings = models.DecimalField(max_digits=6,decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    class Meta:
         unique_together = ("user", "product")
    
class ReviewImage(models.Model):
    review=models.ForeignKey(ProductReview, related_name='review_image',on_delete=models.CASCADE)
    review_image = models.ImageField(upload_to='review_uploads/',blank=True,null=True)
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.review.comments[:10]} by {self.review.user}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('Status_Pending', 'Pending'),
        ('Status_Confirmed', 'Confirmed'),
        ('Status_Shipped', 'Shipped'),
        ('Status_Delivered', 'Delivered'),
        ('Status_Cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="orders")
    
    
    status = models.CharField(max_length=20, default='Status_Pending')
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)        

    def __str__(self):
        return f"Order #{self.id} by {self.user.email} with name {self.user.first_name}"
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):      
        return f"({self.quantity}*) {self.product.name} in Order #{self.order.id} "


class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="shipping_address")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="shipping_address_user")
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"Shipping Address for Order #{self.order.id}"

class BillingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="billing_address")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="billing_address_user",blank=True, null=True)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"Billing Address for Order #{self.order.id}"    


class Payment(models.Model):
    PAYMENT_METHODS=[('Card_type','Credit/Debit Card'),
                     ('COD','Cash on Delivery'),
                     ('E_wallet','Esewa/Khalti'),
                     ]
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    payment_method = models.CharField(max_length=50, choices= PAYMENT_METHODS)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.payment_method}"
    

class Payment(models.Model):
    # ... (Your existing fields: order, payment_method, amount, etc.)

    # --- eSewa Specific Fields ---
    # Store the unique ID generated by *your* system for the transaction
    # This maps to eSewa's 'transaction_uuid'
    transaction_uuid = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    # Store the unique reference ID returned by eSewa/Khalti after payment
    # This maps to eSewa's 'refId' (used in the redirect/verification)
    payment_reference_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    # Store the signature your server generated for verification
    signature = models.CharField(max_length=255, null=True, blank=True)

    # Store the status returned by the server-to-server verification
    is_paid_verified = models.BooleanField(default=False)
    
    # ... (Your existing methods)