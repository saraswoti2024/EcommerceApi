from .models import *
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]

class WishSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ["id", "product"]

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["color","product"]


class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ["id","review_image","created_date"]

class ProductReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()
    review_image= serializers.SerializerMethodField()
    # product = serializers.PrimaryKeyRelatedField(read_only=True)
    uploaded_images= serializers.ListField(
        child= serializers.ImageField(allow_empty_file=False, use_url=True),
        write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = ProductReview
        fields = ["id", "user", "comments","review_image","uploaded_images",  "ratings","replies","reviewed_date"]

    def get_replies(self, obj):
        if obj.replies.exists():
            return ProductReviewSerializer(obj.replies.all(), many=True,context= self.context).data
        return None
    
    def create(self,validated_data):
        uploaded_images= validated_data.pop('uploaded_images', [])
        review= ProductReview.objects.create(**validated_data)
        for image in uploaded_images:
            ReviewImage.objects.create(review=review, review_image=image)
        return review
    
    def update(self, instance, validated_data):
        uploaded_images= validated_data.pop('uploaded_images', [])
        super().update(instance, validated_data)
        if uploaded_images:
            for image in uploaded_images:
                ReviewImage.objects.create(review = instance,review_image= image)
        
        return instance
    
    def get_review_image(self,obj):
        valid_uploaded_image= ReviewImage.objects.filter(review= obj, review_image__isnull= False).exclude(review_image__exact='')
        return ReviewImageSerializer(valid_uploaded_image, many=True, context= self.context).data
    
    def get_user(self,obj):
        return obj.user.first_name