from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from app1.models import Customer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterUserSerializer,LoginUserSerializer,UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from . token import get_token

class RegisterApi(APIView):

    def post(self,request):
        data = request.data
        serializer = RegisterUserSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                'status'  : 200,
                'message' : 'Registration Successfull',
                'data'    :  serializer.data,
            })
        
        return Response({
            'status'  : 400,
            'message' : 'Error',
            'data'    : serializer.errors
        })
    

    
class LoginAPI(TokenObtainPairView):

    def post(self,request,*args,**kwargs):
        email = request.data.get('email')
        password  = request.data.get('password')
        
        user = Customer.objects.get(email = email)
        print(user)

        if not user:
            return Response({'error':' user not found'},status=status.HTTP_404_NOT_FOUND)
              
        if not user.check_password(password):
            return Response({'error':' incorect password'},status=status.HTTP_404_NOT_FOUND)
       
        token = get_token(user)
        serializer = LoginUserSerializer(user)
        return Response({
            'message':'login succesfull',
            'userinfo':serializer.data,
            'token':token
        })

class User_details(APIView):
    def get(self, request):
        try:  
            customers = Customer.objects.filter(is_staff=False).order_by('-id')
            customer_details = []
            for customer in customers:
                customer_details.append({
                    'id': customer.id,
                    'name': customer.username,
                    'email': customer.email,            
                })
            return JsonResponse(customer_details, status=200, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

class UserDeleteView(APIView):
    def delete(self, request, user_id):
        try:       
            customer = Customer.objects.get(id=user_id)
            customer.delete()
            return JsonResponse({'message': 'User deleted successfully'}, status=200)
        except customer.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class AdminLoginView(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            token = get_token(user)

            admin_info = {
                'username': user.username,
                'email': user.email,        
            }
            return JsonResponse({'message': 'Login successful','token': token,'adminInfo': admin_info})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    

class AddUser(APIView):

    def post(self,request):
        data = request.data
        serializer = RegisterUserSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                'status'  : 200,
                'message' : 'Registration Successfull',
                'data'    :  serializer.data,
            })
        
        return Response({
            'status'  : 400,
            'message' : 'Error',
            'data'    : serializer.errors
        })

class AdminSearch(APIView):

    def get(self, request):
        name = request.query_params.get('username', '') 
        print(name,".............")
        if not name:
            return Response({'error': 'Name parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            filtered_names = Customer.objects.filter(name__icontains=name)
            serialized_names = UserSerializer(filtered_names, many=True)
            return Response(serialized_names.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)