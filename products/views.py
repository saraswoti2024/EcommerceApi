from django.shortcuts import render
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from .models import Product,UserChoice,CartItem,WishlistItem
from .serializers import ProductSerializer,UserSerializer,CartSerializer,WishSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework import permissions,status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

class ProductView(APIView):

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
                if request.query_params.get('category'):
                    category = request.query_params.get('category')
                    data = Product.objects.filter(category=category)
                    
                if request.query_params.get('brand'):
                    brand = request.query_params.get('brand')
                    data_brand = data.filter(brand=brand)
                
                if request.query_params.get('rating'):
                    rate = request.query_params.get('rating')
                    data = data_brand.filter(rating=rate)

                page_number = request.GET.get('page', 1)
                paginator_value = Paginator(data , 5)
                serializers = ProductSerializer(paginator_value.page(page_number),many=True)
                return Response(serializers.data,status=status.HTTP_200_OK)
            except Exception as e:
                return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

class ProductViewDetail(APIView):
    def get(self,request,id):
        try:
            value = Product.objects.get(id=id)
            serializers = ProductSerializer(value)
            return Response(serializers.data,status = status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
 

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
        serializer = CartSerializer(product,many=True)
        total_items = CartItem.objects.filter(user=request.user).count()
        return Response({
            "status": "success",
            "message": serializer.data,
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
