from django.shortcuts import render
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from .models import Product,CartItem,WishlistItem,ProductImage,ProductReview,Order,OrderProduct,BillingAddress,ShippingAddress, PaymentESewa,PaymentStatus
from .serializers import ProductSerializer,CartSerializer,WishSerializer,ProductImageSerializer,ProductReviewSerializer,OrderSerializer,BillingAddressSerializer,ShippingAddressSerializer
from rest_framework.views import APIView,View
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework import permissions,status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from products.permissions import CustomBasePermission
from decimal import Decimal
import uuid,base64, hmac, hashlib, json, requests
from django.urls import reverse
from decouple import config
esewa_secret_key = config('ESEWA_SECRET_KEY')
esewa_merchant_product_code = config('MERCHANT_PRODUCT_CODE_ESEWA')


class ProductView(APIView):
    permission_classes = [CustomBasePermission]
    print(permission_classes)

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
                    data = data.filter(brand=brand)
                    total_products = data.filter(brand=brand).count()
                
                if request.query_params.get('rating'):
                    rate = request.query_params.get('rating')
                    total_products = data.filter(rating=rate).count()
                    data = data.filter(rating=rate)

                page_number = request.GET.get('page', 1)
                paginator_value = Paginator(data , 10)
                serializers = ProductSerializer(paginator_value.page(page_number),many=True)
                
                return Response(
                    {'message':serializers.data,
                    "total_products": total_products},
                    status=status.HTTP_200_OK)
            except Exception as e:
                return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
     

class ProductViewDetail(APIView):
    permission_classes = [CustomBasePermission]
    print(permission_classes)

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
    permission_classes  = [CustomBasePermission]
    
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
    permission_classes = [CustomBasePermission]
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
    permission_classes = [CustomBasePermission]
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
    # permission_classes = [CustomBasePermission]
    # def post(self,request):
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
        review = ProductReview.objects.filter(product__id=pk).order_by('-updated')
    # def get(self,request):           
    #     product_id = request.data.get('product_id')
    #     review = ProductReview.objects.filter(product__id=product_id).order_by('-updated')
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



class OrderProductView(APIView):
    permission_classes = [CustomBasePermission]
    print(permission_classes)

    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user).order_by('-order_date')
        serializer = OrderSerializer(orders, many=True)
        return Response({
            "status": "success",
            "total_orders": orders.count(),
            "orders": serializer.data
        }, status=status.HTTP_200_OK)
    

    def post(self,request):
        user = request.user
        no_of_cart_items_raw= request.data.get('no_of_cart_items',[])

        if isinstance(no_of_cart_items_raw, str):
            no_of_cart_items = [int(x) for x in no_of_cart_items_raw.split(',') if x.isdigit()]
        else:
            no_of_cart_items = no_of_cart_items_raw 

        if not no_of_cart_items:
            return Response({"error":"No items in cart is placed for order"},status= status.HTTP_400_BAD_REQUEST)

        selected_cart_items= CartItem.objects.filter(user=user,id__in=no_of_cart_items)

        if not selected_cart_items:
            return Response({ "error":"no cart seleted for order "},status= status.HTTP_400_BAD_REQUEST)
        
        total_price = sum(item.product.price*item.quantity for item in selected_cart_items)
        create_order= Order.objects.create(user=user, total_price= total_price)
        # for item in 

        for item in selected_cart_items:
            OrderProduct.objects.create(
                order=create_order,
                product= item.product,
                quantity= item.quantity,
                price= item.product.price
                )
            item.product.stocks -= item.quantity
            item.product.save()
            
        selected_cart_items.delete()

        

        return Response({
            "message":"order created successfully",
            "order_id": create_order.id,
            "total_price": total_price
        },status=status.HTTP_201_CREATED)


class BillingAddressView(APIView):
    permission_classes= [CustomBasePermission]

    def post(self,request, pk):
        try:
            order = Order.objects.get(id=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BillingAddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, order=order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,pk):
        try:
            order = Order.objects.get(id=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            billing_address = BillingAddress.objects.get(order=order)
        except BillingAddress.DoesNotExist:
            return Response({'error': 'Billing address not found for this order.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BillingAddressSerializer(billing_address)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
class ShippingAddressView(APIView):
    permission_classes= [CustomBasePermission]

    def post(self,request, pk):
        try:
            order = Order.objects.get(id=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ShippingAddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, order=order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

    def get(self,request,pk):
        try:
            order = Order.objects.get(id=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            shipping_address = ShippingAddress.objects.get(order=order)
        except ShippingAddress.DoesNotExist:
            return Response({'error': 'Shipping address not found for this order.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ShippingAddressSerializer(shipping_address)
        return Response(serializer.data, status=status.HTTP_200_OK) 

def generate_signature(key,message):
        key=key.encode('utf-8')
        message = message.encode('utf-8')
        hmac_sha256 = hmac.new(key,message, hashlib.sha256)
        digest= hmac_sha256.digest()
        signature= base64.b64encode(digest).decode('utf-8')
        # print(signature)
        return signature

class CheckoutView(View):
    permission_classes=[CustomBasePermission]

    

    def get(self,request,id):
        order_product= Order.objects.get(id=id)
        
        # product= OrderProduct.objects.all().filter(id=id) 
        # product_code= product.product.code   
        # print(product_code)
        
        #tax_price = tax amount + total price

        tax_amount= ((order_product.total_price) * Decimal('0.13'))
        total_with_tax_price = tax_amount+ order_product.total_price
        print(total_with_tax_price)

        transaction_uuid= uuid.uuid4()
        secret_key = esewa_secret_key
        data_to_sign = f"total_amount={total_with_tax_price},transaction_uuid={transaction_uuid},product_code={esewa_merchant_product_code}"
        result = generate_signature(secret_key,data_to_sign)
        # print(result)
        success_url = request.build_absolute_uri(reverse('payment_success_esewa'))        
        failure_url = request.build_absolute_uri(reverse('payment_failure_esewa'))

        context = {
            'order_product':order_product   ,
            'order_amount':order_product.total_price,
            'tax_amount':tax_amount,
            'total_amount':total_with_tax_price,
            'transaction_uuid':transaction_uuid,
            'product_delivery_charge':0,    
            'product_delivery_charge':0,
            'success_url_esewa':success_url,
            'failure_url_esewa':failure_url,
            'signature':result,

        }
        #PaymentStatus.objects.create(user=request.user,order=order_product,amount=total_with_tax_price,payment_method='E_wallet')
        # if payment_uuid is None:
        #     payment_uuid == transaction_uuid

        
        return render(request,'esewa.html',context)
    

    

class EsewaSuccessView(View):
    def get(self,request):
        # order_product= Order.objects.get(id=id)
        context={}  # Create a dictionary to store the response
        data = request.GET.get('data')  # Get the data from the URL
        # print(data)
        decoded_data = base64.b64decode(data).decode('utf-8')   # Decode the data
        data_dict = json.loads(decoded_data)    # Convert the data to a dictionary
        # Get the values from the dictionary
        total_amount = data_dict['total_amount'] 
        transaction_uuid = data_dict['transaction_uuid']
        product_code = data_dict['product_code']
    
        # Make a request to the eSewa API to get the transaction status
        request_url = f'https://rc.esewa.com.np/api/epay/transaction/status/?product_code={product_code}&total_amount={total_amount}&transaction_uuid={transaction_uuid}'
        response = requests.get(request_url) 
        # print(response)
        response = json.loads(response.text)
        # print(response)
        status = response.get('status')
        # print(status)
        ref_id=response.get('ref_id')
        # print(ref_id)
        user = request.user if request.user.is_authenticated else None
    # {'product_code': 'EPAYTEST', 'transaction_uuid': '02d39d09-d518-40a9-9ac1-6a5a5487fa03', 'total_amount': 1010.0, 'status': 'COMPLETE', 'ref_id': '000CW9X'}
        
        PaymentESewa.objects.create(user=request.user,transaction_uuid=transaction_uuid,product_code=product_code,total_amount=total_amount,status=status,ref_id=ref_id,)

       

        

        

        # CartItem.objects.filter(user=request.user).delete()

        # Put the Status in message key of the context dictionary
        context['message'] = response['status']
        # print(context)
        

        return render(request, 'esewa_success.html',context )
    
    # def patch(request,id):
    #     order_product=
    

class EsewaFailureView(View):
    def get(self, request):
        return render(request, 'esewa_failure.html')





        


# class PaymentView(APIView):
#     permission_classes=[CustomBasePermission]

#     def post(self,request,pk):
#         try:
#             order = Order.objects.et(id= pk,user=request.user)
#         except Order.DoesNotExist:
#             return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = PaymentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(order=order, amount=order.total_price, status='Completed')
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class OrderCreateView(APIView):
#     permission_classes = [CustomBasePermission]
#     print(permission_classes)

#     def post(self,request):
#         try:
#             serializers = OrderSerializer(data = request.data)
#             if serializers.is_valid():
#                     serializers.save(user=request.user)
#                     return Response(serializers.data,status=status.HTTP_201_CREATED)
#             else:
#                 return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response(str(e),status=status.HTTP_400_BAD_REQUEST) 
    
