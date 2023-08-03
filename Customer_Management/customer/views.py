from django.shortcuts import render,redirect
from .models import Product,Customer,Tag,Order
from django.http import HttpResponse
from .forms import *
from .decoration import userUnauthenticated,allowed_user,admin_only
from .filters import OrderFilter

from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from django.contrib import messages
# Create your views here.

@login_required(login_url='login')
@admin_only

def index(request):
    customers=Customer.objects.all()
    orders=Order.objects.all()

    total_order=orders.count()
    deliver=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()

    context={
        'customers':customers,
        'orders' : orders,
        'total_order':total_order,
        'pending':pending,
        'deliver':deliver,
    }
    return render(request,'customer/dashboard.html',context)

"""What User can see in dashboard"""
@login_required(login_url='login')
@allowed_user(allowed_role=['customer'])
def user_page(request):
    orders=request.user.customer.order_set.all()
    total_orders=orders.count()
    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()
    context={
        'orders':orders,
        'total_order':total_orders,
        'delivered':delivered,
        'pending' : pending
    }
    return render(request,'user/user_page.html' , context)
    
"""This is for User settings"""
@allowed_user(allowed_role=['customer'])
@login_required(login_url='login')
def user_settings(request):
    customer=request.user.customer
    form=CustomerForm(instance=customer)
    form.fields['name'].widget.attrs.update({
            'class': "form-control",
        })
    form.fields['phone'].widget.attrs.update({
            'class': "form-control",
        })
    form.fields['email'].widget.attrs.update({
            'class': "form-control",
        })
    form.fields['profile_pic'].widget.attrs.update({
            'class': "form-control",
        })
    
    if request.method=="POST":
        form=CustomerForm(request.POST , request.FILES , instance=customer)
        if form.is_valid():
            form.save()
    context={
        'form':form
    }   
    return render(request , 'user/user_settings.html' , context) 

"""Registration and login """
@userUnauthenticated
def Registration(request):
    form=RegForm()
    form.fields['username'].widget.attrs.update({
            'placeholder': '  Username',
            'class': "form-control",
        })
    form.fields['email'].widget.attrs.update({
            'placeholder': ' name@example.com',
            'class': "form-control",
        })
    form.fields['password1'].widget.attrs.update({
            'placeholder': ' Password',
            'class': "form-control",
        })
    form.fields['password2'].widget.attrs.update({
            'placeholder': ' Re-enter Password',
            'class': "form-control",
        })
    if request.method=="POST":
        form=RegForm(request.POST)

        if form.is_valid():
            user=form.save()
            username =form.cleaned_data.get('username')

            messages.success(request, 'Registration completed for '+username)
            return redirect('login')
    context={
        'form':form
    }
    return render(request , 'user/registration.html',context)

@userUnauthenticated
def user_login(request):
    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username or password is incorrect')
    context={
        
    }
    return render(request,'user/login.html',context)

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_user(allowed_role=['admin'])

def customer(request,pk):
    customers=Customer.objects.get(id=pk)
    orders=customers.order_set.all()
    total_order=orders.count()

    myFilter=OrderFilter(request.GET , queryset=orders)
    orders=myFilter.qs

    context={
        'total_order':total_order,
        'orders' : orders,
        'customers':customers,
        'myfilter':myFilter,
    }
    return render(request,'customer/customer.html',context)

@login_required(login_url='login')
@allowed_user(allowed_role=['admin'])
def product(request):
    products=Product.objects.all()
    context={
        'products':products,
    }
    return render(request,'customer/product.html',context)

@login_required(login_url='login')
@allowed_user(allowed_role=['admin'])

def create_order(request):
    form=OrderForm()
    if request.method == "POST":
        form=OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={
        'form':form
    }
    return render(request,'form/order_form.html',context) 

"""def customer_create_order(request,pk_c_o):
    customer=Customer.objects.get(id=pk_c_o)
    form=OrderForm(initial={'customer':customer})
    if request.method == "POST":
        form=OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={
        'form':form
    }
    return render(request,'form/customer_create_order.html',context) """

###for inline form set

@login_required(login_url='login')
def customer_create_order(request,pk_c):
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'))
    customer=Customer.objects.get(id=pk_c)
    formset=OrderFormSet(instance=customer)
    if request.method=="POST":
        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
        else:
            return HttpResponse('Form is not valid')
    context={
        'formset':formset
    }    
    return render(request,'form/customer_create_order.html',context)        

@login_required(login_url='login')
@allowed_user(allowed_role=['admin'])

def update_order(request ,pk_up):
    order = Order.objects.get(id=pk_up)
    form=OrderForm(instance=order)
    if request.method == "POST":
        form=OrderForm(request.POST , instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={
        'form':form
    }
    return render(request , 'form/order_form.html',context)

@login_required(login_url='login')
@allowed_user(allowed_role=['admin'])

def remove_order(request,pk_remove):
    order=Order.objects.get(id=pk_remove)
    item=Order.objects.all()
    if request.method =="POST":
        order.delete()
        return redirect('/')
    context={
        'order':order,
        'item':item
    }
    return render(request , 'form/delete_order.html',context)

'''def customer_remove_order(request,pk_c_r_o):
    order=Order.objects.get(id=pk_c_r_o)
    customer=Customer.objects
    if request.method=="POST":
        order.delete()
        return redirect('/customer/')
    context={
        'order':order
    }
    return render(request , 'customer_stats/customer_order_remove.html' , context)'''
