"""
URL configuration for self_storage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from warehouse_app import views
from django.conf import settings
from django.conf.urls.static import static
from promo.views import tracked_redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('faq/', views.faq, name='faq'),
    path('boxes/', views.boxes, name='boxes'),
    path('my-rent/', views.profile_view, name='my-rent'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('promo/<slug:slug>/', tracked_redirect, name='tracked_redirect'),
    path('qr_code/', views.qr_code, name='qr_code'),
    path('create_order', views.create_order, name='create_order'),
    path('extend-order/<int:order_id>/', views.extend_order, name='extend_order'),

]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
