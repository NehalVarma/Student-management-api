from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    Permission class to check if user is an admin.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin


class IsTeacherUser(BasePermission):
    """
    Permission class to check if user is a teacher.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_teacher


class IsStudentUser(BasePermission):
    """
    Permission class to check if user is a student.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_student_user


class IsAdminOrTeacher(BasePermission):
    """
    Permission class to check if user is admin or teacher.
    """
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and 
                (request.user.is_admin or request.user.is_teacher))


class IsOwnerOrAdminOrTeacher(BasePermission):
    """
    Permission class to check if user is the owner or admin/teacher.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow admin and teachers full access
        if request.user.is_admin or request.user.is_teacher:
            return True
        
        # Allow owner access (if object has user field)
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # Allow access to own profile
        if hasattr(obj, 'id') and obj.id == request.user.id:
            return True
            
        return False


class IsReadOnlyOrAdminOrTeacher(BasePermission):
    """
    Permission class that allows read-only access for students,
    full access for admin and teachers.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
            
        # Admin and teachers have full access
        if request.user.is_admin or request.user.is_teacher:
            return True
            
        # Students have read-only access
        if request.user.is_student_user:
            return request.method in ['GET', 'HEAD', 'OPTIONS']
        
        return False