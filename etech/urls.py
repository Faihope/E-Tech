from django.conf.urls import url
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
   path('',views.index,name='index'),
   path('register/',views.registeruser,name='registeruser'),
   path('loginuser/', views.loginpage, name="loginuser"), 
   path('logout/',views.logoutuser,name='logout'),
   path('<int:id>/',views.detail,name='detail'),
   path('checkout/',views.checkout,name='checkout'),
   path('cart/',views.cart,name='cart'),
   path('update/',views.updateItem,name='update_item'),
   path('profile/<int:id>/',views.profile,name='profile'),
   path('updateprofile/',views.updateprofile,name='updateprofile'),


   





]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
