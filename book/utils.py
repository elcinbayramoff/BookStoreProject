from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()


def has_role(user, role):
    """
    Check if user has a specific role.
    
    Args:
        user: User instance
        role: Role string ('admin', 'seller', 'customer')
    
    Returns:
        bool: True if user has the role, False otherwise
    """
    if not user or not user.is_authenticated:
        return False
    return user.role == role


def has_any_role(user, roles):
    """
    Check if user has any of the specified roles.
    
    Args:
        user: User instance
        roles: List of role strings
    
    Returns:
        bool: True if user has any of the roles, False otherwise
    """
    if not user or not user.is_authenticated:
        return False
    return user.role in roles


def is_admin(user):
    """Check if user is an admin."""
    return has_role(user, 'admin')


def is_seller(user):
    """Check if user is a seller."""
    return has_role(user, 'seller')


def is_customer(user):
    """Check if user is a customer."""
    return has_role(user, 'customer')


def is_seller_or_admin(user):
    """Check if user is a seller or admin."""
    return has_any_role(user, ['seller', 'admin'])


def can_manage_books(user):
    """
    Check if user can manage books based on their role.
    
    Args:
        user: User instance
    
    Returns:
        bool: True if user can manage books
    """
    if not user or not user.is_authenticated:
        return False
    
    if user.role == 'admin':
        return True
    elif user.role == 'seller':
        return True
    elif user.role == 'customer':
        return False
    
    return False


def can_apply_discount(user):
    """
    Check if user can apply discounts to books.
    
    Args:
        user: User instance
    
    Returns:
        bool: True if user can apply discounts
    """
    return is_seller_or_admin(user)


def can_manage_authors(user):
    """
    Check if user can manage authors.
    
    Args:
        user: User instance
    
    Returns:
        bool: True if user can manage authors (only admins)
    """
    return is_admin(user)


def can_manage_categories(user):
    """
    Check if user can manage categories.
    
    Args:
        user: User instance
    
    Returns:
        bool: True if user can manage categories (only admins)
    """
    return is_admin(user)


def get_user_permissions(user):
    """
    Get a dictionary of all permissions for a user.
    
    Args:
        user: User instance
    
    Returns:
        dict: Dictionary containing permission flags
    """
    if not user or not user.is_authenticated:
        return {
            'can_view_books': False,
            'can_create_books': False,
            'can_update_books': False,
            'can_delete_books': False,
            'can_apply_discount': False,
            'can_manage_authors': False,
            'can_manage_categories': False,
        }
    
    return {
        'can_view_books': True,  # All authenticated users can view
        'can_create_books': is_seller_or_admin(user),
        'can_update_books': is_seller_or_admin(user),
        'can_delete_books': is_seller_or_admin(user),
        'can_apply_discount': can_apply_discount(user),
        'can_manage_authors': can_manage_authors(user),
        'can_manage_categories': can_manage_categories(user),
    }
