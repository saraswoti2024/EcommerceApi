from django.urls import path
from .views import ProductView,ProductViewDetail,Cart,RemoveCart

urlpatterns = [
    path('product/',ProductView.as_view(),name="productview"),
    path('productdetail/<int:id>/',ProductViewDetail.as_view(),name="productviewdetail"),
    path('addcart/',Cart.as_view(),name="addtocart"),
    path('removecart/<int:id>/',RemoveCart.as_view(),name="removecart"),
]