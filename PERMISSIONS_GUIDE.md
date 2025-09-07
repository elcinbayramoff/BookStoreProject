# Django Permissions and Authorization Guide

This guide explains the permission system implemented in the BookStore project and how to use role-based access control.

## Overview

The project implements a comprehensive permission system with three user roles:
- **Admin**: Full access to all operations
- **Seller**: Can manage books and apply discounts
- **Customer**: Can only view books, authors, and categories

## Permission System Architecture

### 1. User Roles

The `User` model extends Django's `AbstractUser` with a custom role field:

```python
class Role(models.TextChoices):
    CUSTOMER = 'customer', 'Customer'
    SELLER = 'seller', 'Seller'
    ADMIN = 'admin', 'Admin'
```

### 2. Custom Permission Classes

Located in `book/permissions.py`, these classes control access to different operations:

#### `CanManageBooks`
- Controls access to book management operations
- Admins: Full access
- Sellers: Can create, update, view books
- Customers: View only

#### `CanApplyDiscount`
- Controls access to discount operations
- Only sellers and admins can apply discounts

#### `CanManageAuthors`
- Controls access to author management
- Only admins can create/update/delete authors

#### `CanManageCategories`
- Controls access to category management
- Only admins can create/update/delete categories

#### `IsSellerOrAdmin`
- General permission for seller/admin operations
- Used for book creation, updates, and deletions

### 3. ViewSet Permission Implementation

Each ViewSet implements role-based permissions using the `get_permissions()` method:

```python
def get_permissions(self):
    if self.action == 'list' or self.action == 'retrieve':
        # Allow any authenticated user to view
        permission_classes = [permissions.IsAuthenticated]
    elif self.action in ['create', 'update', 'partial_update', 'destroy']:
        # Only sellers and admins can modify
        permission_classes = [permissions.IsAuthenticated, IsSellerOrAdmin]
    else:
        permission_classes = self.permission_classes
    
    return [permission() for permission in permission_classes]
```

## API Endpoint Permissions

### Book Endpoints (`/api/books/`)

| Method | Endpoint | Description | Admin | Seller | Customer |
|--------|----------|-------------|-------|--------|----------|
| GET | `/api/books/` | List books | ✓ | ✓ | ✓ |
| GET | `/api/books/{id}/` | Retrieve book | ✓ | ✓ | ✓ |
| POST | `/api/books/` | Create book | ✓ | ✓ | ✗ |
| PUT | `/api/books/{id}/` | Update book | ✓ | ✓ | ✗ |
| PATCH | `/api/books/{id}/` | Partial update | ✓ | ✓ | ✗ |
| DELETE | `/api/books/{id}/` | Delete book | ✓ | ✓ | ✗ |
| POST | `/api/books/{id}/discount/` | Apply discount | ✓ | ✓ | ✗ |
| GET | `/api/books/most_discounted_books/` | Most discounted | ✓ | ✓ | ✓ |

### Author Endpoints (`/api/authors/`)

| Method | Endpoint | Description | Admin | Seller | Customer |
|--------|----------|-------------|-------|--------|----------|
| GET | `/api/authors/` | List authors | ✓ | ✓ | ✓ |
| GET | `/api/authors/{id}/` | Retrieve author | ✓ | ✓ | ✓ |
| POST | `/api/authors/` | Create author | ✓ | ✗ | ✗ |
| PUT | `/api/authors/{id}/` | Update author | ✓ | ✗ | ✗ |
| PATCH | `/api/authors/{id}/` | Partial update | ✓ | ✗ | ✗ |
| DELETE | `/api/authors/{id}/` | Delete author | ✓ | ✗ | ✗ |
| POST | `/api/authors/{id}/change_name/` | Change name | ✓ | ✗ | ✗ |

### Category Endpoints (`/api/categories/`)

| Method | Endpoint | Description | Admin | Seller | Customer |
|--------|----------|-------------|-------|--------|----------|
| GET | `/api/categories/` | List categories | ✓ | ✓ | ✓ |
| GET | `/api/categories/{id}/` | Retrieve category | ✓ | ✓ | ✓ |
| POST | `/api/categories/` | Create category | ✓ | ✗ | ✗ |
| PUT | `/api/categories/{id}/` | Update category | ✓ | ✗ | ✗ |
| PATCH | `/api/categories/{id}/` | Partial update | ✓ | ✗ | ✗ |
| DELETE | `/api/categories/{id}/` | Delete category | ✓ | ✗ | ✗ |
| POST | `/api/categories/{id}/update_name/` | Update name | ✓ | ✗ | ✗ |

## Utility Functions

Located in `book/utils.py`, these functions help with permission checking:

### Role Checking Functions
- `has_role(user, role)`: Check if user has specific role
- `has_any_role(user, roles)`: Check if user has any of the specified roles
- `is_admin(user)`: Check if user is admin
- `is_seller(user)`: Check if user is seller
- `is_customer(user)`: Check if user is customer
- `is_seller_or_admin(user)`: Check if user is seller or admin

### Permission Checking Functions
- `can_manage_books(user)`: Check if user can manage books
- `can_apply_discount(user)`: Check if user can apply discounts
- `can_manage_authors(user)`: Check if user can manage authors
- `can_manage_categories(user)`: Check if user can manage categories

### Helper Function
- `get_user_permissions(user)`: Get all permissions for a user as a dictionary

## Usage Examples

### 1. Using Permission Classes in Views

```python
from rest_framework import viewsets
from .permissions import CanManageBooks, IsSellerOrAdmin

class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, CanManageBooks]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsSellerOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
```

### 2. Using Utility Functions

```python
from book.utils import can_manage_books, get_user_permissions

def some_view(request):
    if can_manage_books(request.user):
        # User can manage books
        pass
    
    permissions = get_user_permissions(request.user)
    if permissions['can_apply_discount']:
        # User can apply discounts
        pass
```

### 3. Custom Action Permissions

```python
@action(detail=True, methods=['post'], url_path='discount', permission_classes=[CanApplyDiscount])
def apply_discount(self, request, pk=None):
    # Only users with CanApplyDiscount permission can access this
    pass
```

## Testing Permissions

Run the test script to verify permissions work correctly:

```bash
python test_permissions.py
```

This will:
1. Create test users with different roles
2. Test utility functions
3. Test permission classes
4. Simulate API endpoint permissions

## Best Practices

1. **Always check authentication first**: Ensure users are authenticated before checking permissions
2. **Use specific permissions**: Create granular permissions for different operations
3. **Test thoroughly**: Always test permissions with different user roles
4. **Document permissions**: Keep clear documentation of what each role can do
5. **Use utility functions**: Leverage utility functions for consistent permission checking

## Security Considerations

1. **Never trust client-side permissions**: Always validate permissions on the server
2. **Use HTTPS**: Ensure all API communications are encrypted
3. **Regular audits**: Periodically review and audit permission assignments
4. **Principle of least privilege**: Give users only the minimum permissions they need
5. **Monitor access**: Log permission checks for security auditing

## Extending the Permission System

To add new permissions:

1. Create a new permission class in `book/permissions.py`
2. Add utility functions in `book/utils.py`
3. Update ViewSets to use the new permissions
4. Update documentation
5. Add tests

Example:

```python
class CanManageInventory(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'seller']
```
