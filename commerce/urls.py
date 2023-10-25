"""commerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("auctions.urls")),
    #path('auth/', include(('django.contrib.auth.urls','auth'), namespace='auth')),
    #path("accounts/login/", auth_views.LoginView.as_view(template_name="auctions/llogin.html")),
    #path('password_reset/', auth_views.PasswordResetView.as_view(template_name="auctions/password_reset.html"), name='password_reset'),
    #path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]


admin.site.site_header="Auctions Adminstrations"
admin.site.site_title="Auctions"
admin.site.index_title="Auctions"
admin.site.index_template="auctions/custom_admin_index.html"