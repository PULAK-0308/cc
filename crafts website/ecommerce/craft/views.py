from math import ceil
from django.shortcuts import get_object_or_404, render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.template import loader
from datetime import datetime
from django.contrib import messages
from .models import Product,Orders
from PayTm import Checksum
from django.views.decorators.csrf import csrf_exempt
MERCHANT_KEY = 'kbzk1DSbJiV_03p5'

# Create your views here.

def index(request):
    
    return render(request,'index.html')

def register(request):
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user=User.objects.filter(username=username)#ye apan ne isiliye likha jisse agar manlo apan ne register ke time pe same username dalke submit kara to unique constraint ka error na ye
        if user.exists():
            messages.info(request,"Username already taken")
            return redirect('register')
             
        
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        
        
        user.set_password(password)#this is done so that password is encrypted
        user.save()
        
        messages.info(request,'Account created succesfully')
        
        return redirect('register')
        
    return render(request,'register.html')
    
    

def loginuser(request):
    if request.method=="POST":
        
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():#ye check karne ke liye ki iss username se user exists karta h ya nhi
            messages.info(request,"Invalid Username ")
            return redirect('loginuser')
        
        user=authenticate(username=username,password=password)#agar username ya password galat hua to ye None return karega
        
        if user is None:
            messages.info(request,"Invalid Password")
            return redirect('loginuser')
        
        else:
            login(request,user)
            return redirect('mainpage')
            
            
        
    return render(request,'index.html')

def logoutuser(request):
    logout(request)
    return redirect('loginuser')

         
     
@login_required(login_url="loginuser")
def mainpage(request):
    return render(request,'mainpage.html')

@login_required(login_url="loginuser")
def dreamcatchers(request):
    products=Product.objects.all()
    
    allProds=[]
    catprods=Product.objects.values('category','id')
    #print(catprods)
    cats={item['category'] for item in catprods}
    #print("categories are ",cats)
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        print(prod)
        n=len(prod)
        nslides=n//4 + ceil((n/4)-(n//4))
        allProds.append([prod,range(1,nslides),nslides])
        #print(allProds) 
    params={'allProds':allProds}
    return render(request,'dreamcatchers.html',params)

# @login_required(login_url="loginuser")
# def resinproducts(request):
#     products=Product.objects.all()
#     print(products)
#     return render(request,'resinproducts.html',context={'products':products})


    

def checkout(request):
    thank=False
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone,amount=amount)
        order.save()
        
        thank = True
        id = order.order_id
        param_dict = {

                'MID': 'muFqPO48357187186180',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest',

        }
        
        #return render(request, 'checkout.html', {'thank':thank, 'id': id})
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'paytm.html', {'param_dict': param_dict})
    return render(request, 'checkout.html')


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})


    
@login_required(login_url="loginuser")
def gallery(request):
    
    
    return render(request,'gallery.html')