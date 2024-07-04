from django.urls import path
from products.api.view import ProductView, FileUploadView

urlpatterns = [
    path('products', ProductView.as_view(), name='products'),
    path('files', FileUploadView.as_view(), name='files')
]   