from django.http import JsonResponse
from django.shortcuts import redirect, render
from . models import Customer, Product, Cart, OrderPlaced
from django.views import View
from.forms import CustomerRegistrationForm,CustomerProfileForm, PaymentForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
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
  item_allready_in_cart=False
  if request.user.is_authenticated:
   item_allready_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
  return render (request,'Shop/productdetail.html',{'product':product, 'item_allready_in_cart': item_allready_in_cart})
  
 

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

@login_required
def orders(request):
 op=OrderPlaced.objects.filter(user=request.user)
 return render(request, 'Shop/orders.html',{'order_placed':op})

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
@method_decorator(login_required,name='dispatch')
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
   
@login_required 
def checkout(request):
 user=request.user
 add=Customer.objects.filter(user=user)
 cart_items=Cart.objects.filter(user=user)
 amount=0.0
 shipping_amount=130.0
 totalamount=0.0
 cart_product=[p for p in Cart.objects.all() if p.user==user]
 for p in cart_product:
    tempamount=(p.quantity * p.product.discounted_price)
    amount+=tempamount
    totalamount=amount+shipping_amount
 return render(request, 'Shop/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})

 

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
 
# def payment_page(request):
#  if request.method == 'POST':
#   form = PaymentForm(request.POST)
#   if form.is_valid():
#    payment_method = form.cleaned_data.get('payment_method')
   
#    # Validate payment method specific fields
#    if payment_method in ['CC', 'DC']:
#     card_number = form.cleaned_data.get('card_number')
#     cvv = form.cleaned_data.get('cvv')
#     if not card_number or not cvv:
#      messages.error(request, 'Card details are required')
#      return redirect('payment-page')
#    elif payment_method == 'MB':
#     mobile_number = form.cleaned_data.get('mobile_number')
#     if not mobile_number:
#      messages.error(request, 'Mobile number is required')
#      return redirect('payment-page')
   
#    # Store payment method in session
#    request.session['payment_method'] = payment_method
#    request.session['payment_status'] = 'Completed'
   
#    return redirect('payment-done')
#  else:
#   form = PaymentForm()
 
#  return render(request, 'Shop/payment.html', {'form': form})

@login_required
def payment_done(request):
 user=request.user
 custid=request.GET.get('custid')
 customer=Customer.objects.get(id=custid)
 cart=Cart.objects.filter(user=user)
 
 
 for c in cart:
  OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,).save()
  c.delete()
 
 messages.success(request, f'Order placed successfully! Payment method: {payment_method}')
 return redirect("orders")