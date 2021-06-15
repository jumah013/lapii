from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from .models import User,Fan,Customer
from .form import CustomerSignUpForm,FanSignUpForm
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm

from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder

#pdf
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

#email
from django.core.mail import send_mail


# Create your views here.
def homepage(request):
	if request.user.is_authenticated:
		if request.user.is_fan:
			return redirect('fan')
		else:
			return redirect('store')
	return render(request,'pages/home.html')
	
def home(request):
  
    return render(request, 'pages/index.html')

def register(request):
    return render(request, 'pages/register.html')

class customer_register(CreateView):
    model = User
    form_class= CustomerSignUpForm
    template_name= 'pages/customer_register.html'

    def form_valid(self, form):
        user=form.save()
        login(self.request,user)
        return redirect('login')


class fan_register(CreateView):
    model = User
    form_class= FanSignUpForm
    template_name= 'pages/employee_register.html'

    def form_valid(self, form):
        user=form.save()
        login(self.request,user)
        return redirect('login')

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid Username or Password')
        else:
            messages.error(request, 'Invalid Username or Password')
    return render(request, 'pages/login.html',
     context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/')

def Customerpage(request):
    return render(request,'pages/customer.html')
def Fanpage(request):
    return render(request,'pages/fan.html')

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'pages/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'pages/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'pages/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

# TICKET DETAILS
def details(request):
	if request.method == "POST":
		your_name =request.POST['name']
		your_phone =request.POST['phone']
		your_email =request.POST['email']
		your_match =request.POST['match']
		your_date =request.POST['date']
		your_price =request.POST['price']
		
		buy = "Name: "+ your_name + " Phone: " +  your_phone + "Email:" +  your_email + "Match:" + your_match + "price:" + your_price + "Date:" + your_date 


		send_mail(
            'Ticket Information',#subject111
            buy,#message
            your_email,#from email
            ['jumabenjamin17@gmail.com'],# to email
        )

		return render(request,'pages/details.html',{
			'your_name' : your_name,
			'your_phone' : your_phone,
			'your_email' : your_email,
			'your_match' : your_match,
			'your_date' : your_date,
			'your_price' : your_price,

		})
	else:
		return render(request,'pages/store.html')
def paypal(request):
	return render(request,'pages/paypal.html')
# pdf views

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None


data = {
	"company": "Dennnis Ivanov Company",
	"address": "123 Street name",
	"city": "Vancouver",
	"state": "WA",
	"zipcode": "98663",


	"phone": "555-555-2345",
	"email": "youremail@dennisivy.com",
	"website": "dennisivy.com",
	}

#Opens up page as PDF
class ViewPDF(View):
	def get(self, request, *args, **kwargs):

		pdf = render_to_pdf('pages/pdf_template.html', data)
		return HttpResponse(pdf, content_type='application/pdf')


#Automaticly downloads to PDF file
class DownloadPDF(View):
	def get(self, request, *args, **kwargs):
		
		pdf = render_to_pdf('pages/pdf_template.html', data)

		response = HttpResponse(pdf, content_type='application/pdf')
		filename = "Invoice_%s.pdf" %("12341231")
		content = "attachment; filename='%s'" %(filename)
		response['Content-Disposition'] = content
		return response
