from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
import json
# Create your views here.
def index(request):
     
    allProds = []
    catProds = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n//4 + ceil((n//4)-(n/4))
        allProds.append([prod,range(1,nSlides),nSlides])
    params = {'allProds' : allProds}
    return render(request, 'shop/index.html', params)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    if request.method=="POST":
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        contact = Contact(name=name, email=email, phn=phone, desc=desc)
        contact.save()
    return render(request, 'shop/contact.html')

def tracker(request):
    if request.method=="POST":
        order_id = request.POST.get('order_id','')
        email = request.POST.get('email','')
        # return HttpResponse(f"{order_id} and {email}")
        try:
            order = Orders.objects.filter(order_id=order_id, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=order_id)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc, 'time':item.timestamp})
                    response = json.dumps(updates, default=str)
                # print(response)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')
    return render(request, 'shop/tracker.html')

def search(request):
    return HttpResponse("at search")

def productView(request,myid):
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodView.html', {'product':product[0]})

def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson','')
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        address = request.POST.get('address1','') + ", " + request.POST.get('address2','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip_code','')
        phone = request.POST.get('phone','')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="This order is placed")
        update.save()
        id = order.order_id
        thank = True
        return render(request, 'shop/checkout.html', {'thank':thank , 'id':id})
    return render(request, 'shop/checkout.html')