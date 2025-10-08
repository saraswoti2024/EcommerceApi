from django.contrib import admin
from .models import *
from accounts.models import CustomUser
# Register your models here.

admin.site.register([Product, Category, Brand, ProductImage,ProductReview,CustomUser, ReviewImage])
