from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import Product, Category
from django.contrib.auth.models import User
from .serializer import ProductSerializer, CategorySerializer
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
 
        # Add custom claims
        token['username'] = user.username
        # ...
 
        return token
 
 
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@permission_classes([IsAuthenticated])
class Product_view(APIView):
    """
    This class handle the CRUD operations for MyModel
    """
    def get(self, request):
        """
        Handle GET requests to return a list of MyModel objects
        """
        my_model = Product.objects.all()
        serializer = ProductSerializer(my_model, many=True)
        return Response(serializer.data)


    def post(self, request):
        """
        Handle POST requests to create a new Product object
        """
        # usr =request.user
        # print(usr)
        serializer = ProductSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def put(self, request, pk):
        """
        Handle PUT requests to update an existing Product object
        """
        my_model = Product.objects.get(pk=pk)
        serializer = ProductSerializer(my_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@permission_classes([IsAuthenticated])
class Category_view(APIView):
    """
    This class handle the CRUD operations for MyModel
    """
    def get(self, request):
        """
        Handle GET requests to return a list of MyModel objects
        """
        my_model = Category.objects.all()
        serializer = CategorySerializer(my_model, many=True)
        return Response(serializer.data)


    def post(self, request):
        """
        Handle POST requests to create a new Category object
        """
        # usr =request.user
        # print(usr)
        serializer = CategorySerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def put(self, request, pk):
        """
        Handle PUT requests to update an existing Category object
        """
        my_model = Category.objects.get(pk=pk)
        serializer = CategorySerializer(my_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def purchase(request):
    user = request.user
    price = request.data['price']
    cart = request.data['cart']
    totalPrice = 0

    supermarket_p = Product.objects.all()

    for item_id, item_info in cart.items():
        try:
            product = Product.objects.get(id=item_info['id'])
            if product:
                if product.price == item_info['price']:
                    itemprice = item_info['price']
                    totalPrice += (itemprice * item_info['count'])
                else:
                    print("Warning, Wrong Price")
                    return Response({"state":"fail", "msg":"ERROR, Something went wrong."})
            else:
                print("Warning, Unauthorized Item Detected.")
                return Response({"state":"fail", "msg":"ERROR, Something went wrong."})
        except ObjectDoesNotExist:
            print(f"Warning, Unauthorized Item Detected {item_info['id']}.")
            return Response({"state":"fail", "msg":"ERROR, Something went wrong."})

    if totalPrice == price:
        print("Purchase Completed")
        return Response({"state":"success", "msg":f"Purchase Complete, You Bought All The Specificed Items For ${totalPrice}"})
    else:
        print(f"Warning Wrong Price Client Reported: {price} , Server Calculated: {totalPrice}")
        return Response({"state":"fail", "msg":"Purchase Failed"})


# @api_view(['POST'])
# def register(request):
#     if request.method == "POST":
#         # Validate and serialize the request data (you can use serializers for this)
#         username = request.data.get("username")
#         password = request.data.get("password")

#         if not username or not password:
#             return Response({'error': 'Username and password are required fields.'}, status=400)

#         try:
#             # Create a new user
#             user = User.objects.create_user(username=username, password=password)
#             return Response({'message': 'User created successfully'}, status=201)
#         except Exception as e:
#             return Response({'error': 'Failed to create user', 'details': str(e)}, status=400)

# # Create your views here.
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def products(req):
#     if req.method == 'GET':
#         products = ProductSerializer(Product.objects.all(), many=True).data
#         return Response(products)
    

