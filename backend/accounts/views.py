from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .serializers import UserSerializer, AccountSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
# Create your views here.


@api_view(['POST'])
def register(request):
    data = request.data
    user = AccountSerializer(data=data)
    if user.is_valid():
        if not User.objects.filter(username=data['username']).exists():
            user = User.objects.create(
                username=data['username'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=make_password(data['password'])
            )
            user.save()
            return Response({'success': 'user created successfully!'}, status=status.HTTP_201_CREATED)
            
        else:
            return Response({'error': 'user is not valid!'}, status=status.HTTP_400_BAD_REQUEST)     
    else:
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def currentUser(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def update_profile(request):
    user = request.user
    data = request.data

    # Use serializer for validation
    serializer = UserSerializer(user, data=data, partial=True)

    if serializer.is_valid():
        if data.get('password'):
            user.password = make_password(data['password'])
        
        # Update other fields
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.username = data.get('username', user.username)
        
        user.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




