from django.http import JsonResponse
from django.shortcuts import redirect, render
from . models import Customer, Product, Cart, OrderPlaced
from django.views import View
from.forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
# Create your views here.
class ProductView(View):
 def get(self, request):
  gentspants = Product.objects.filter(category='GP')
  sares = Product.objects.filter(category='S')
  borkhs = Product.objects.filter(category='BK')
  lehengas=Product.objects.filter(category='L')
  babyfashions = Product.objects.filter(category='BF')
  return render(request, 'Shop/home.html', {'gentspants':gentspants, 'sares':sares,'borkhs':borkhs,'lehengas':lehengas,'babyfashions':babyfashions})

#def product_detail(request):
# return render(request, 'Shop/productdetail.html')

class ProductDetail(View):
 def get(self,request,pk):
  product=Product.objects.get(pk=pk)
  return render (request,'Shop/productdetail.html',{'product':product})
  
 

def add_to_cart(request):
 user=request.user
 product_id=request.GET.get('product_id')
 product=Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 return redirect('/cart')



def show_cart(request):
 if request.user.is_authenticated:
  user=request.user
  cart=Cart.objects.filter(user=user)
  amount=0.0
  shipping_amount=130.0
  total_amount=0.0
  cart_product=[p for p in Cart.objects.all() if p.user==user]
  if cart_product:
   for p in cart_product:
    tempamount=(p.quantity * p.product.discounted_price)
    amount+=tempamount
   total_amount=amount+shipping_amount
  else:
    return render(request, 'Shop/emptycart.html')
  return render(request, 'Shop/addtocart.html',{'carts':cart,'totalamount':total_amount,'amount':amount})
  

def buy_now(request):
 return render(request, 'Shop/buynow.html')

def profile(request):
 return render(request, 'Shop/profile.html')

def address(request):
 add=Customer.objects.filter(user=request.user)
 return render(request, 'Shop/address.html',{'add':add,'active':'btn-primary'})
 return render(request, 'Shop/address.html')

def orders(request):
 return render(request, 'Shop/orders.html')

def change_password(request):
 return render(request, 'Shop/changepassword.html')

def lehenga(request,data=None):
 if data==None:
  lehengas=Product.objects.filter(category='L')
 elif data=="pakija" or data=="ponnoala":
  lehengas=Product.objects.filter(category='L').filter(brand=data)
 elif data=="below":
  lehengas=Product.objects.filter(category='L').filter(discounted_price__lt=2000)
 elif data=="above":
  lehengas=Product.objects.filter(category='L').filter(discounted_price__gt=2000)
 return render(request, 'Shop/lehenga.html',{'lehengas':lehengas})

#def login(request):
     #return render(request, 'Shop/login.html')

#def customerregistration(request):
 #return render(request, 'Shop/customerregistration.html')
class CustomerRegistrationView(View):
 def get(self,request):
  form=CustomerRegistrationForm()
  return render(request, 'Shop/customerregistration.html',{'form':form})
 def post(self, request):
  form=CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request,'Congratulations registration successfully done')
   form.save()
   return render(request, 'Shop/customerregistration.html',{'form':form})
  else:
   return render(request, 'Shop/customerregistration.html',{'form':form})
  
# def profile(request):
#  return render(request, 'Shop/profile.html')

class CustomerProfileView(View):
 def get(self,request):
  form=CustomerProfileForm()
  return render(request, 'Shop/profile.html',{'form':form,'active':'btn-primary'})
 
 
 def post(self, request):
  form=CustomerProfileForm(request.POST)
  if form.is_valid():
   usr=request.user
   name=form.cleaned_data['name']
   division=form.cleaned_data['division']
   district=form.cleaned_data['district']
   thana=form.cleaned_data['thana']
   villorroad=form.cleaned_data['villorroad']
   zipcode=form.cleaned_data['zipcode']
   reg=Customer(user=usr,name=name,division=division,district=district,thana=thana,villorroad=villorroad,zipcode=zipcode)
   reg.save()
   messages.success(request,'Congratulations profile updated successfully')
  return render(request, 'Shop/profile.html',{'form':form,'active':'btn-primary'})
   
def checkout(request):

 return render(request, 'Shop/checkout.html')

# Ajax plus cart
def plus_cart(request):
 if request.method=='GET':
  prod_id=request.GET['prod_id']
  c=Cart.objects.get(Q(product__id=prod_id) & Q(user=request.user))
  c.quantity+=1
  c.save()
  amount=0.0
  shipping_amount=130.0
  cart_product=[p for p in Cart.objects.all() if p.user==request.user]
  for p in cart_product:
   tempamount=(p.quantity * p.product.discounted_price)
   amount+=tempamount
  totalamount=amount+shipping_amount
  data={
   'quantity':c.quantity,
   'amount':amount,
   'totalamount':totalamount
  }
  return JsonResponse(data)

# Ajax minus cart
def minus_cart(request):
 if request.method=='GET':
  prod_id=request.GET['prod_id']
  c=Cart.objects.get(Q(product__id=prod_id) & Q(user=request.user))
  c.quantity-=1
  c.save()
  amount=0.0
  shipping_amount=130.0
  cart_product=[p for p in Cart.objects.all() if p.user==request.user]
  for p in cart_product:
   tempamount=(p.quantity * p.product.discounted_price)
   amount+=tempamount
  totalamount=amount+shipping_amount
  data={
   'quantity':c.quantity,
   'amount':amount,
   'totalamount':totalamount
  }
  return JsonResponse(data)

# Ajax remove cart
def remove_cart(request):
 if request.method=='GET':
  prod_id=request.GET['prod_id']
  c=Cart.objects.get(Q(product__id=prod_id) & Q(user=request.user))
  c.delete()
  amount=0.0
  shipping_amount=130.0
  cart_product=[p for p in Cart.objects.all() if p.user==request.user]
  for p in cart_product:
   tempamount=(p.quantity * p.product.discounted_price)
   amount+=tempamount
  totalamount=amount+shipping_amount
  data={
   'amount':amount,
   'totalamount':totalamount
  }
  return JsonResponse(data)
 