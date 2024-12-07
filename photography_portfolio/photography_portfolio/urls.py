from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from portfolio_app import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Public pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),

    # User authentication
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('forgot_password/', auth_views.PasswordResetView.as_view(template_name='forgot_password.html'), name='forgot_password'),

    # Protected pages
    path('my_works/', views.my_works, name='my_works'),  # This will require login
    path('upload_image/', views.upload_image, name='upload_image'),
    path('edit/<int:image_id>/', views.update_image, name='update_image'),  # Add this
    path('delete/<int:image_id>/', views.delete_image, name='delete_image'),
]   

if settings.DEBUG:  # Only serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
