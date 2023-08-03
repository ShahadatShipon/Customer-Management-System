from django.contrib import admin
from django.urls import path

from django.contrib.auth import views as auth_view

from . import views
urlpatterns = [
    path('' , views.index , name='dashboard'),
    path('user/',views.user_page ,name='user') ,
    path('user_settings' , views.user_settings , name="user_settings"),
    path('customer/<str:pk>' ,views.customer ,name='customer'),
    path('product/',views.product,name='product'),
    path('order_form/', views.create_order ,name='order_form'),
    path('customer_create_order/<str:pk_c>' , views.customer_create_order ,name='customer_create_order'),
    path('update_form/<str:pk_up>' , views.update_order ,name='update_form'),
    path('remove_form/<str:pk_remove>' , views.remove_order ,name='remove_form'),
    # path('customer_remove_order/<str:pk_c_r_o>' , views.customer_remove_order ,name='customer_remove_order'),
    path('reg/' ,views.Registration,name='reg'),
    path('login/' ,views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),

    ###Reset password with email
    path('reset_password/',auth_view.PasswordResetView.as_view(
                            template_name ='password_reset/password_reest.html'), name='reset_password'),
    path('password_reset_done/',auth_view.PasswordResetDoneView.as_view(
                            template_name ='password_reset/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>' , auth_view.PasswordResetConfirmView.as_view(
                            template_name ='password_reset/password_reset_form.html'), name='password_reset_confirm'),
    path('password_reset_complete/',auth_view.PasswordResetCompleteView.as_view(
                            template_name ='password_reset/password_reset_done.html'), name='password_reset_complete'),
    

]