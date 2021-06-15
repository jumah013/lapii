from django.urls import path
from .import views

urlpatterns=[
    path('',views.homepage,name='home'),
    path('index/',views.home,name='index'),
    path('register/',views.register,name='register'),
    path('customer_register/',views.customer_register.as_view(),name='customer_register'),
    path('employee_register/',views.fan_register.as_view(),name='employee_register'),
    path('login/',views.login_request,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('customer/',views.Customerpage,name='customer'),
    path('fan/',views.Fanpage,name='fan'),
    path('details/', views.details, name="details"),
    path('paypal/', views.paypal, name="paypal"),

    path('store/', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

    # pdf url

	
    path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),

    
  

]