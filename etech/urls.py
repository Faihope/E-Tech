from django.conf.urls import url
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
   path('',views.index,name='index'),
   path('register/',views.registeruser,name='registeruser'),
   path('login/', views.loginpage, name="login"), 
   path('logout/',views.logoutuser,name='logout'),
   path('<int:id>/',views.detail,name='detail'),
   path('checkout/',views.checkout,name='checkout'),
   path('cart/',views.cart,name='cart'),
   path('update/',views.updateItem,name='update_item'),





]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
