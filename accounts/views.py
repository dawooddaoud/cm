from django.shortcuts import render,redirect
from .models import *
from django.urls import reverse_lazy
from .forms import OrderForm, CreateUserForm, CustomerForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users , admin_only
from django.contrib.auth.models import Group
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('accounts:home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('accounts:login')



@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name = 'customer')
            user.groups.add(group)
            Customer.objects.create(user=user)


            messages.success(request, f'Signed up successfully {username}')
            return redirect('accounts:login')
    context = {'form':form}
    return render(request,'accounts/register.html',context)


@login_required(login_url='accounts:login')
@admin_only
@allowed_users(allowed_roles =['admin'] )
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    total_customers = orders.count()
    delivered = orders.filter(status = "Delivered").count()
    pending = orders.filter(status = "Pending").count()

    context = {
        'customers':customers,
        'orders': orders,
        'total_orders': total_orders,
        'pending': pending,
        'delivered':delivered,
        'total_customers':total_customers,

    }
    return render(request,'accounts/dashboard.html',context)


@login_required
@allowed_users(allowed_roles='customer')
def userPage(request):

    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    pending = orders.filter(status = "Pending").count()
    delivered = orders.filter(status = "Delivered").count()
    context = {
        "orders":orders,
        'total_orders': total_orders,
        'pending': pending,
        'delivered':delivered,
    }
    return render(request,"accounts/user.html",context)



@login_required
@allowed_users(allowed_roles='customer')
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES,instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request,'Change Has Been Saved! ')
            
    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='accounts:login')    
@allowed_users(allowed_roles =['admin'] )
def products(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request,'accounts/products.html',context)




@login_required(login_url='accounts:login')
@allowed_users(allowed_roles =['admin'] )
def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    orders_count = orders.count()
    filter = OrderFilter(request.GET, queryset = orders)
    orders =filter.qs
    context = {
        'customer':customer,
        'orders': orders,
        'orders_count':orders_count,
        'filter':filter,
    }
    return render(request,'accounts/customer.html',context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles =['admin'] )
def done(request):
    return render(request,'accounts/done.html')


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles =['admin'] )
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer, Order,fields=('product','status'), extra = 10
        )

    customer = Customer.objects.get(id = pk)
    formset = OrderFormSet(queryset= Order.objects.none(),instance = customer)
    if request.method == "POST":
        formset = OrderFormSet(request.POST, instance = customer)
        if formset.is_valid():
            formset.save()
            return redirect('/done')
    context = {
        'formset':formset,
    }
    return render(request, 'accounts/order_form.html', context)



@login_required(login_url='accounts:login')
@allowed_users(allowed_roles =['admin'] )
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form }
    return render(request, 'accounts/update_form.html', context)



@login_required(login_url='accounts:login')
@allowed_users(allowed_roles =['admin'] )
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'accounts/delete_order.html', context)