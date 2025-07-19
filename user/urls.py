from django.urls import path
from . import views

urlpatterns = [
    path('debug/<int:id>/<str:word>/', views.debug_view),
    path('users/', views.user_list),
    path('users/<int:id>/', views.user_detail),
]