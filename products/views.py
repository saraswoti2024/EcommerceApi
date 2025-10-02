from django.shortcuts import render
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from .models import Product
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework import permissions,status

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