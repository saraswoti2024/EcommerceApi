from django.shortcuts import render
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from .models import Product,CartItem,WishlistItem,ProductImage,ProductReview
from .serializers import ProductSerializer,CartSerializer,WishSerializer,ProductImageSerializer,ProductReviewSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework import permissions,status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class ProductView(APIView):

    #admin
    def post(self,request):
        try: 
            serializers = ProductSerializer(data = request.data)
            if serializers.is_valid():
                    serializers.save()
                    return Response(serializers.data,status=status.HTTP_201_CREATED)
            else:
                return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)


    def get(self,request):
            try:
                data = Product.objects.all()
                total_products = Product.objects.all().count()
                if request.query_params.get('category'):
                    category = request.query_params.get('category')
                    data = Product.objects.filter(category=category)
                    total_products = Product.objects.filter(category=category).count()

                if request.query_params.get('brand'):
                    brand = request.query_params.get('brand')
                    data_brand = data.filter(brand=brand)
                    total_products = data.filter(brand=brand).count()
                
                if request.query_params.get('rating'):
                    rate = request.query_params.get('rating')
                    total_products = data_brand.filter(rating=rate).count()
                    data = data_brand.filter(rating=rate)

                page_number = request.GET.get('page', 1)
                paginator_value = Paginator(data , 5)
                serializers = ProductSerializer(paginator_value.page(page_number),many=True)
                
                return Response(
                    {'message':serializers.data,
                    "total_products": total_products},
                    status=status.HTTP_200_OK)
            except Exception as e:
                return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
     

class ProductViewDetail(APIView):
    def get(self,request,id):
        try:
            value = Product.objects.get(id=id)
            if request.query_params.get('color'):
                color = request.query_params.get('color')
                product_color = ProductImage.objects.filter(color=color,product__id = value.id)
                serializers = ProductImageSerializer(product_color,many=True)
            else:
                serializers = ProductSerializer(value)
            return Response(serializers.data,status = status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

    #admin
    def patch(self,request,id):
        try: 
            product1 = Product.objects.get(id=id)
            serializers = ProductSerializer(product1,data = request.data,partial=True)
            if serializers.is_valid():
                    serializers.save()
                    return Response(serializers.data,status=status.HTTP_201_CREATED)
            else:
                return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request,id):
        try:
            product1 = Product.objects.get(id=id)
            product1.delete()
            product_count = Product.objects.all().count()
            return Response(
                {
                    "status": "success",
                    "message": "product_deleted",
                    "product_count": product_count
                },
                status=status.HTTP_200_OK
            )
        except Product.DoesNotExist:
            return Response({"status": "error", "message": "Item not in cart"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                

class Cart(APIView):
    permission_classes = [IsAuthenticated] 
    def post(self,request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity',1))
        product = get_object_or_404(Product,id=product_id)
        cart_item , created = CartItem.objects.get_or_create(
            user = request.user,
            product = product,
            defaults = {'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        serializer = CartSerializer(cart_item)
        total_items = CartItem.objects.filter(user=request.user).count()

        return Response({
            "status": "success",
            "message": "Item added to cart" if created else "Quantity updated",
            "cart_item": serializer.data,
            "cart_count": total_items
        }, status=status.HTTP_201_CREATED)

    def get(self,request):
        product = CartItem.objects.filter(user=request.user)
        total_items = CartItem.objects.filter(user=request.user).count()
        page_number = request.GET.get('page', 1)
        paginator_value = Paginator(product , 5)
        serializers = CartSerializer(paginator_value.page(page_number),many=True)
        return Response({
            "status": "success",
            "message": serializers.data,
            "cart_count": total_items
        }, status=status.HTTP_201_CREATED)       

class RemoveCart(APIView):

    def delete(self,request,id):
        product = get_object_or_404(Product,id=id)
        try:
            cart_item = CartItem.objects.get(user=request.user,product=product)
            cart_item.delete()
            cart_count = CartItem.objects.filter(user=request.user).count()
            return Response(
                {
                    "status": "success",
                    "message": "Item removed from cart",
                    "cart_count": cart_count
                },
                status=status.HTTP_200_OK
            )
        except CartItem.DoesNotExist:
            return Response({"status": "error", "message": "Item not in cart"},
                    status=status.HTTP_400_BAD_REQUEST
                )

class Wishlist(APIView):
    def post(self,request):
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product,id=product_id)
        wish_item , created = WishlistItem.objects.get_or_create(
            user = request.user,
            product = product,
        )
        serializer = WishSerializer(wish_item)
        total_items = WishlistItem.objects.filter(user=request.user).count()

        return Response({
            "status": "success",
            "message": "wish items",
            "wish_item": serializer.data,
            "cart_count": total_items
        }, status=status.HTTP_201_CREATED)
    
    def get(self,request):
        product = WishlistItem.objects.filter(user=request.user)
        paginator_value = Paginator(product , 5)
        total_items = WishlistItem.objects.filter(user=request.user).count()
        page_number = request.GET.get('page', 1)
        serializers = WishSerializer(paginator_value.page(page_number),many=True)
        return Response({
            "status": "success",
            "message": serializers.data,
            "wishlist_count": total_items
        }, status=status.HTTP_201_CREATED) 
    
    def delete(self,request):
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product,id=product_id)
        try:
            wish_item = WishlistItem.objects.get(user=request.user,product=product)
            wish_item.delete()
            wishlist_count = WishlistItem.objects.filter(user=request.user).count()
            return Response(
                {
                    "status": "success",
                    "message": "Item removed from wishlist",
                    "cart_count": wishlist_count,
                },
                status=status.HTTP_200_OK
            )
        except WishlistItem.DoesNotExist:
            return Response({"status": "error", "message": "Item not in wishlist"},
                    status=status.HTTP_400_BAD_REQUEST
                )

class ProductReviewView(APIView):
    def post(self,request,pk):
        try:
            # product_id = request.data.get('product_id')
            productr = Product.objects.get(id=pk)
            serializer = ProductReviewSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save(user=request.user,product=productr)
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,pk):           
        # product_id = request.data.get('product_id')
        review = ProductReview.objects.filter(product__id=pk)
        serializer = ProductReviewSerializer(review,many=True)
        return Response(serializer.data)
    
    def patch(self,request,pk):
        # product_id = request.data.get('product_id')
        review = ProductReview.objects.get(product__id=pk,user=request.user)       
        serializer = ProductReviewSerializer(review,data = request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    
class ProductReviewReplyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,pk):
        try:
            replies=ProductReview.objects.get(id=pk)
        except ProductReview.DoesNotExist:
            return Response({'error': 'No review like this '},status.HTTP_404_NOT_FOUND)
        
        serializer= ProductReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, reply=replies, product=replies.product)
            return Response({"message": "victory to create reply ","reply_id":serializer.instance.id}, status.HTTP_201_CREATED
                        )
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
