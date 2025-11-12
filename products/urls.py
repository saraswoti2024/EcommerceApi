from django.urls import path
from .views import ProductView,ProductViewDetail,Cart,RemoveCart,Wishlist,ProductReviewView,ProductReviewReplyView,OrderProductView,ShippingAddressView,BillingAddressView,CheckoutView,EsewaSuccessView,EsewaFailureView

urlpatterns = [
    path('product/',ProductView.as_view(),name="productview"),
    path('productdetail/<int:id>/',ProductViewDetail.as_view(),name="productviewdetail"),
    path('addcart/',Cart.as_view(),name="cart"),
    path('removecart/<int:id>/',RemoveCart.as_view(),name="removecart"),
    path('addwishlist/',Wishlist.as_view(),name="wishlist"),
    path('review/<int:pk>/',ProductReviewView.as_view(),name="review"),
    path('review/reply/<int:pk>/',ProductReviewReplyView.as_view(),name="review_reply"),
    path('review/',ProductReviewView.as_view(),name="productreviewview"),
    path('order/',OrderProductView.as_view(),name="orderproductview"),
    path('order/shipping/<int:pk>/',ShippingAddressView.as_view(),name="ordershippingview"),
    path('order/billing/<int:pk>/',BillingAddressView.as_view(),name="orderbillingview"),
    path('order/checkout/esewa/<int:id>/',CheckoutView.as_view(),name ="order_checkout"),
    path('order/checkout/esewa/success/', EsewaSuccessView.as_view(), name='payment_success_esewa'),
    path('order/checkout/esewa/failure/', EsewaFailureView.as_view(), name='payment_failure_esewa'),

   
    
    
    # path('checkout/',OrderProductCheckoutView.as_view(),name="orderproductcheckoutview"),
]