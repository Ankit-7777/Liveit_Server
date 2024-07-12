from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from rest_framework.decorators import action
from core.models import Category
from core.permissions import IsSuperuserOrReadOnly
from core.serializers import CategorySerializer
from core.pagination import MyPageNumberPagination
from core.renderers import UserProfileRenderer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    renderer_classes = [UserProfileRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperuserOrReadOnly]

    def list(self,request):
        sub_category = request.query_params.get('sub_category')
        if sub_category == 'True':
            queryset = self.queryset.filter(sub_category=True)
        elif sub_category  == 'False':
            queryset = self.queryset.filter(sub_category=False)
        else:
            queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response({"message": "Category updated successfully", "category_detail": serializer.data},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    def partial_update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response({"message": "Category partially updated successfully", "category_detail": serializer.data},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @action(detail=False, methods=['GET'], name='category_name_search')
    def search(self, request):
        search_str = request.query_params.get('search_str')
        if not search_str:
            return Response({"message": "Search query cannot be empty"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        queryset = Category.objects.all()
        search_str = search_str.lower()
        queryset = queryset.filter(category_name__icontains=search_str)
        
        if not queryset.exists():
            return Response({"message": "No categories found for the provided search query"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

