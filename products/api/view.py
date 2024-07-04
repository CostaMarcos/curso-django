from rest_framework.views import APIView
from products.models import Product, FileUpload
from products.api.serializer import ProductSerializer, FileUploadSerializer
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework import status
import os
from django.conf import settings
import pandas as pd

class ProductView(APIView):
    def get(self, request, id=None):
        product_model = Product.objects.all()
        
        if(id):
            _products = product_model.filter(id=id)
            _products = ProductSerializer(data=_products)

            _products.is_valid()
            return Response(data=_products.data, status=status.HTTP_200_OK)
            
        _products = ProductSerializer(data=product_model)
        _products.is_valid()
        return Response(data=_products.data, status=status.HTTP_200_OK)

class FileUploadView(APIView):

    def get(self, request):
        file_name = request.GET.get('filename', '')
        if(file_name):
            file_instance = FileUpload.objects.filter(file__icontains=file_name).order_by('-id').first()
            file_handle = open(os.path.join(settings.BASE_DIR, file_instance.file.name), 'rb')
            file_response = FileResponse(file_handle)
            return file_response
        return Response(data={'message': 'É necessário enviar o nome do arquivo'}, status=status.HTTP_404_NOT_FOUND)
    

    def post(self, request):
        try:
            _file = FileUploadSerializer(data=request.data)
            _file.is_valid(raise_exception=True)
            file_instance = _file.save()

            # pd.read_csv(os.path.)
            file_path = os.path.join(settings.BASE_DIR, file_instance.file.name)
            try:
                csv = pd.read_csv(file_path)
                print(csv.to_dict())
            except:
                pass

            return Response(data={'filename': file_instance.file.name}, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(data={'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    