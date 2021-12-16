"""
Definition of urls for DjangoWebProject1.
"""

from datetime import datetime
from django.urls import path, re_path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView

from app import forms, views

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Вход',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('pool/', views.pool, name='pool'),
    path('registration', views.registration, name='registration'),
    path('blog/', views.blog, name='blog'),
    path('chooseSide/', views.chooseSide, name='chooseSide'),
    path('shop/', views.shop, name='shop'),
    path('shop/<str:parameter>/', views.shop, name='shop'),
    path('product/<int:parameter>/', views.productPage, name='product'),
    path('newpost/', views.newpost, name='newpost'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('total_price/<int:orderId>/', views.total_price, name='total_price'),
    path('quantity_minus/', views.quantity_minus, name='quantity_minus'),
    path('quantity_plus/', views.quantity_plus, name='quantity_plus'),
    path('deal_order/', views.deal_order, name='deal_order'),
    path('delete_item/<int:item>/', views.delete_item, name='delete_item'),
    path('orders/', views.orders, name='orders'),
    path('myorders/', views.myOrders, name='myOrders'),
    path('orderdetails/<int:orderId>/', views.orderDetails, name='orderDetails'),
    path('deleteorder/', views.delete_order, name='deleteOrder'),

    re_path(r'^(?P<parameter>\d+)/$', views.blogpost, name='blogpost'),
]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()