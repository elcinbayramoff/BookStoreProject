from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to edit, but allow read access to all authenticated users.
    """
    
    def has_permission(self, request, view):
        # Read permissions for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Write permissions only for admin users
        return request.user.is_authenticated and request.user.role == 'admin'


class IsSellerOrAdmin(BasePermission):
    """
    Custom permission to only allow sellers and admins to perform certain actions.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        return request.user.role in ['seller', 'admin']


class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Write permissions only for the owner or admin
        return request.user.is_authenticated and (
            request.user.role == 'admin' or 
            hasattr(obj, 'user') and obj.user == request.user
        )


class CanManageBooks(BasePermission):
    """
    Custom permission for book management based on user role.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Define what each role can do
        if request.user.role == 'admin':
            return True  # Admin can do everything
        
        elif request.user.role == 'seller':
            # Sellers can create, update, and view books
            return request.method in ['GET', 'POST', 'PUT', 'PATCH']
        
        elif request.user.role == 'customer':
            # Customers can only view books
            return request.method in permissions.SAFE_METHODS
        
        return False


class CanApplyDiscount(BasePermission):
    """
    Custom permission to only allow sellers and admins to apply discounts.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        return request.user.role in ['seller', 'admin']


class CanManageAuthors(BasePermission):
    """
    Custom permission for author management.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Only admins can manage authors
        return request.user.role == 'admin'


class CanManageCategories(BasePermission):
    """
    Custom permission for category management.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Only admins can manage categories
        return request.user.role == 'admin'
