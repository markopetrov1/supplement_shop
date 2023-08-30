"""
URL configuration for supplement_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from supplement_shop import settings
from supplements import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("supplements/<int:supplement_id>/", views.supplement_details, name="supplement-detail"),
    path("supplements/edit/<int:supplement_id>/", views.edit_supplement, name="edit-supplement"),
    path("supplements/add/", views.add_supplement, name="add-supplement"),
    path("shopping-cart", views.shopping_cart, name="shopping-cart"),
    path("logout", views.logout_request, name="logout"),
    path("payment-info", views.payment_info, name="payment-info"),
    path("confirm-payment", views.confirm_payment, name="confirm-payment"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
