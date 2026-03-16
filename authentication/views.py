from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db import models
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserProfileSerializer,
    UserProfileDetailSerializer,
    ChangePasswordSerializer
)
from .models import User
from .permissions import IsAdminUser, IsAdminOrTeacher


def get_tokens_for_user(user):
    """
    Generate JWT tokens for a user
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration(request):
    """
    Register a new user
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        
        return Response({
            'success': True,
            'message': 'User registered successfully',
            'user': UserProfileSerializer(user).data,
            'tokens': tokens
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'Registration failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """
    Login user and return JWT tokens
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        tokens = get_tokens_for_user(user)
        
        return Response({
            'success': True,
            'message': 'Login successful',
            'user': UserProfileSerializer(user).data,
            'tokens': tokens
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'Login failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Get current user's profile
    """
    serializer = UserProfileDetailSerializer(request.user)
    return Response({
        'success': True,
        'message': 'Profile retrieved successfully',
        'data': serializer.data
    })


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update current user's profile
    """
    serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'message': 'Profile updated successfully',
            'data': serializer.data
        })
    
    return Response({
        'success': False,
        'message': 'Profile update failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Change user password
    """
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Generate new tokens after password change
        tokens = get_tokens_for_user(user)
        
        return Response({
            'success': True,
            'message': 'Password changed successfully',
            'tokens': tokens
        })
    
    return Response({
        'success': False,
        'message': 'Password change failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminOrTeacher])
def user_list(request):
    """
    Get list of all users (Admin and Teacher only)
    """
    users = User.objects.all()
    
    # Filter by role if specified
    role = request.GET.get('role')
    if role and role in ['ADMIN', 'TEACHER', 'STUDENT']:
        users = users.filter(role=role)
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        users = users.filter(
            models.Q(username__icontains=search) |
            models.Q(email__icontains=search) |
            models.Q(first_name__icontains=search) |
            models.Q(last_name__icontains=search)
        )
    
    serializer = UserProfileSerializer(users, many=True)
    return Response({
        'success': True,
        'message': 'Users retrieved successfully',
        'data': serializer.data,
        'count': len(serializer.data)
    })


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def user_detail(request, pk):
    """
    Get, update or delete a specific user (Admin only)
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({
            'success': False,
            'message': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserProfileDetailSerializer(user)
        return Response({
            'success': True,
            'message': 'User retrieved successfully',
            'data': serializer.data
        })
    
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'User updated successfully',
                'data': serializer.data
            })
        return Response({
            'success': False,
            'message': 'User update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        user.delete()
        return Response({
            'success': True,
            'message': 'User deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    Get dashboard statistics based on user role
    """
    user = request.user
    
    stats = {
        'user_info': UserProfileSerializer(user).data,
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(is_active=True).count(),
    }
    
    # Add role-specific stats
    if user.is_admin or user.is_teacher:
        from students.models import Student
        stats.update({
            'total_students': Student.objects.count(),
            'users_by_role': {
                'admins': User.objects.filter(role='ADMIN').count(),
                'teachers': User.objects.filter(role='TEACHER').count(),
                'students': User.objects.filter(role='STUDENT').count(),
            }
        })
    
    return Response({
        'success': True,
        'message': 'Dashboard stats retrieved successfully',
        'data': stats
    })
