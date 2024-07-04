from rest_framework.serializers import ModelSerializer
from products.models import Product, FileUpload

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class FileUploadSerializer(ModelSerializer):
    class Meta:
        model = FileUpload
        fields = "__all__"