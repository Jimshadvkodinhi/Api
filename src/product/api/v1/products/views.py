from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from users.models import *
from api.v1.products.serializers import *
from rest_framework import status


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_category(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Category created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Product created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_products(request):
    products = Product.objects.all()
    category_id = request.query_params.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    sort_by_price = request.query_params.get('sort')
    if sort_by_price == 'low_to_high':
        products = products.order_by('price')
    elif sort_by_price == 'high_to_low':
        products = products.order_by('-price')
    search_query = request.query_params.get('search')
    if search_query:
        products = products.filter(name__icontains=search_query)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)