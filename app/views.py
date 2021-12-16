"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect, reverse
from django.http import HttpRequest
from .forms import MyRequestForm
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.db import models
from .models import Blog
from .models import Comment
from .models import Shop
from .models import Orders
from .models import SubOrders
from .models import UserProfile
from .forms import CommentForm
from .forms import BlogForm


def home(request):
    """Renders the home page."""
    posts = Blog.objects.all().reverse()[:6]
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'posts' : posts,
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Свяжитесь с нами',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Здесь вы найдете!',
            'year':datetime.now().year,
        }
    )


def pool(request):
    """Renders the request page."""
    assert isinstance(request, HttpRequest)
    data = None

    if request.method == 'POST':
        form = MyRequestForm(request.POST)
        if form.is_valid():
            data = dict()
            data['theme'] = form.cleaned_data['requestTheme']
            data['text'] = form.cleaned_data['requestText']
            data['choice'] = form.cleaned_data['requestChoice']
            data['radio'] = form.cleaned_data['requestRadio']
            data['email'] = form.cleaned_data['requestMail']
            form = None
    else:
        form = MyRequestForm()

    return render(
        request,
        'app/pool.html',
        {
            'form' : form,
            'data' : data,
            'title':'Обратная связь',
            'message' : 'Оставьте сообщение об ошибке.',
            'year':datetime.now().year,
        }
    )

def registration(request):
        if request.method == "POST":
            regform = UserCreationForm(request.POST)
            if regform.is_valid():
                reg_f = regform.save(commit=False)
                reg_f.is_staff = False
                reg_f.is_active = True
                reg_f.is_superuser = False
                reg_f.date_joined = datetime.now()
                reg_f.last_login = datetime.now()
                regform.save()
                return redirect('home')
        else:
           regform =  UserCreationForm()
           
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/registration.html',
            {
                'title': 'Регистрация',
                'regform' : regform,
                'year':datetime.now().year,
                }
            )
def blog(request):
    """Renders the blog page."""
    posts = Blog.objects.all()
   
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title':'Блог',
            'posts': posts,
            'year':datetime.now().year,
        }
    )
def blogpost(request, parameter):
    """Renders the blog page."""
    post = Blog.objects.get(id=parameter)
    comments = Comment.objects.filter(post=parameter)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = Blog.objects.get(id=parameter)
            comment_f.save()
            return redirect('blogpost', parameter=post.id)
                
    else:
        form = CommentForm()
        


    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blogpost.html',
        {
            
            'post': post,
            'comments': comments,
            'form': form,
            'year':datetime.now().year,
        }
    )
def newpost(request):

    if request.method == 'POST':
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.author = request.user
            blog_f.posted = datetime.now()
            blog_f.save()
            return redirect('blog')
                
    else:
        blogform = BlogForm()
        


    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/newpost.html',
        {
            
            'blogform': blogform,
            'year':datetime.now().year,
        }
    )



def chooseSide(request):
    currentUser = UserProfile.objects.get(user = request.user)
    currentUser.choosedSide = request.GET.get('side')
    currentUser.save()
    return redirect(reverse('home'))
    


def shop(request, parameter = None):
    """Renders the shop page."""
    if parameter == None:
        products = Shop.objects.all()
    else:
        products = Shop.objects.filter(category = parameter)


    currentProducts = Paginator(products, 6)
    page = request.GET.get('page')
    Products = currentProducts.get_page(page)
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/shop.html',
        {
            'title':'Магазин',
            'products': Products,
            'year':datetime.now().year,
        }
    )


def productPage(request, parameter):
    currentProduct = Shop.objects.get(id = parameter)

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/productPage.html',
        {
            'title':'Товар',
            'item': currentProduct,
            'year':datetime.now().year,
        }
    )

def cart(request):
    currentOrder, status = Orders.objects.get_or_create(holder = request.user, status = 'incart')
    currentProducts = SubOrders.objects.filter(order = currentOrder)

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/cart.html',
        {
            'title':'Корзина',
            'status':'cart',
            'items': currentProducts,
            'order': currentOrder,
            'year':datetime.now().year,
        }
    )

def add_to_cart(request):

    current_product = Shop.objects.filter(id = request.GET.get('product')).first()
    current_order, status = Orders.objects.get_or_create(holder=request.user, status='incart')
    if status:
        current_order.save()
    suborder, status = SubOrders.objects.get_or_create(order=current_order, product=current_product)
    if status: 
        suborder.price = suborder.product.price * suborder.quantity
        suborder.save()
    else:
        suborder.quantity += 1
        suborder.price = suborder.product.price * suborder.quantity
        suborder.save()
    order_list = SubOrders.objects.filter(order=current_order)
    current_order.total_price = 0
    for item in order_list:
        current_order.total_price += item.price

    current_order.save()
    assert isinstance(request, HttpRequest)
    return redirect(reverse('shop'))


def total_price(request, orderId):

    current_order = Orders.objects.get(id = orderId)
    order_list = SubOrders.objects.filter(order=current_order)
    current_order.total_price = 0
    for item in order_list:
        current_order.total_price += item.price

    current_order.save()
    
    if current_order.status == 'incart':
        return redirect(reverse('cart'))
    else:
        return redirect(reverse('orderDetails', kwargs={'orderId': orderId}))

def delete_item(request, item):
    current_item = SubOrders.objects.get(id = item).delete()
    return redirect(reverse('total_price', kwargs={'orderId': current_item.order.id}))

def quantity_minus(request):
    current_item = SubOrders.objects.filter(id = request.GET.get('item')).first()
 
    current_item.quantity -= 1
    if current_item.quantity == 0:
        return redirect(reverse('delete_item', kwargs={'item': current_item.id}))
    else:

        current_item.price = current_item.product.price * current_item.quantity
        current_item.save()
    
        return redirect(reverse('total_price', kwargs={'orderId': current_item.order.id }))

def quantity_plus(request):
    current_item = SubOrders.objects.filter(id = request.GET.get('item')).first()
 
    current_item.quantity += 1
    current_item.price = current_item.product.price * current_item.quantity
    current_item.save()
    
    return redirect(reverse('total_price', kwargs={'orderId': current_item.order.id}))

def deal_order(request):
    current_order = Orders.objects.filter(holder=request.user, status='incart').first()
    current_order.status = 'check'
    current_order.save()
    
    return redirect(reverse('shop'))

def orders(request):
    current_orders = Orders.objects.all().exclude(status = 'incart')
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/orders.html',
        {
            'status': 'admins',
            'title':'Заказы',
            'orders': current_orders,
            'year':datetime.now().year,
        }
    )

def myOrders(request):
    current_orders = Orders.objects.filter(holder = request.user).exclude(status = 'incart')
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/orders.html',
        {
            'status': 'user',
            'title':'Мои заказы',
            'orders': current_orders,
            'year':datetime.now().year,
        }
    )

def orderDetails(request, orderId):
    currentOrder = Orders.objects.get(id = orderId)
    currentProducts = SubOrders.objects.filter(order = currentOrder)

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/cart.html',
        {
            'title':'Заказ',
            'status':'edit',
            'items': currentProducts,
            'order': currentOrder,
            'year':datetime.now().year,
        }
    )

def delete_order(request):
    current_item = Orders.objects.get(id = request.GET.get('order')).delete()
    return redirect(reverse('shop'))