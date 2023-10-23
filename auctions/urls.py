from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),    
    path("create_listing/",views.create_listing,name="create_listing"),
    path("listing/<int:id_listing>",views.listing,name='listing'),
    path("watchlist/",views.watchlist,name='watchlist'),
    path('delete_from_watchlist/<int:id_listing>',views.delete_from_watchlist,name="delete_from_watchlist"),
    path('categories/',views.categories,name='categories'),
    path('category/<int:cat>',views.category,name='category'),
    path('change_status/<int:id_listing>',views.change_status,name='change_status'),
]
