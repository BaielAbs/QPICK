from django.urls import path
from . import views

urlpatterns = [
    path('', views.tehno_start, name='tehno_start'),
    path('register/', views.tehno_register, name='tehno_register'),
    path('login/', views.tehno_login, name='tehno_login'),
    path('catalog/', views.tehno_list, name='index'),
    path('basket/', views.tehno_basket, name='tehno_basket'),
    path('basket/add/<int:pk>/', views.cart_add, name='cart_add'),
    path('basket/remove/<int:pk>/', views.cart_remove, name='cart_remove'),
    path('basket/delete/<int:pk>/', views.cart_delete_item, name='cart_delete_item'),
    path('product/<int:pk>/', views.tehno_detail, name='tehno_detail'),
    path('product/create/', views.tehno_create, name='tehno_create'),
    path('product/<int:pk>/edit/', views.tehno_edit, name='tehno_edit'),
    path('product/<int:pk>/delete/', views.tehno_delete, name='tehno_delete'),
    path('fav/', views.tehno_fav, name='tehno_fav'),
    path('fav/toggle/<int:pk>/', views.fav_toggle, name='fav_toggle'),
    path('checkout/', views.tehno_checkout, name='tehno_checkout'),
    path('profile/', views.tehno_profile, name='tehno_profile'),
]