from django.urls import path
from .views import ProductView,ProductViewDetail,Cart,RemoveCart,Wishlist,ProductReviewView

urlpatterns = [
    path('product/',ProductView.as_view(),name="productview"),
    path('productdetail/<int:id>/',ProductViewDetail.as_view(),name="productviewdetail"),
    path('addcart/',Cart.as_view(),name="cart"),
    path('removecart/<int:id>/',RemoveCart.as_view(),name="removecart"),
    path('addwishlist/',Wishlist.as_view(),name="wishlist"),
    path('review/',ProductReviewView.as_view(),name="productreviewview"),
]