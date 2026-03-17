from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Student
from .serializers import StudentSerializer


@api_view(['GET', 'POST'])
def student_list(request):
    if request.method == 'GET':
        students = Student.objects.all()
        
        # Search functionality
        search = request.GET.get('search')
        if search:
            students = students.filter(name__icontains=search)
        
        course = request.GET.get('course')
        if course:
            students = students.filter(course__icontains=course)
            
        age = request.GET.get('age')
        if age:
            students = students.filter(age=age)
        
        serializer = StudentSerializer(students, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'count': len(serializer.data),
            'message': 'Students retrieved successfully'
        })

    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Student created successfully'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'errors': serializer.errors,
            'message': 'Failed to create student'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Student retrieved successfully'
        })

    elif request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = StudentSerializer(student, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Student updated successfully'
            })
        return Response({
            'success': False,
            'errors': serializer.errors,
            'message': 'Failed to update student'
        }, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student.delete()
        return Response({
            'success': True,
            'message': 'Student deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def search_students(request):
    query = request.GET.get('q', '')
    if not query:
        return Response({
            'success': False,
            'message': 'Search query parameter "q" is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    students = Student.objects.filter(
        name__icontains=query
    ) | Student.objects.filter(
        course__icontains=query
    )
    
    serializer = StudentSerializer(students, many=True)
    return Response({
        'success': True,
        'data': serializer.data,
        'count': len(serializer.data),
        'query': query,
        'message': f'Found {len(serializer.data)} students matching "{query}"'
    })