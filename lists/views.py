from django.shortcuts import render
from django.http      import HttpResponse
from django.shortcuts import render, redirect
from lists.models     import Item
# Create your views here.
def home_page(request):
    if request.POST:
        new_item_text = request.POST['item_text']
        item          = Item.objects.create(text=new_item_text)
        item.save()
        return redirect('/')
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})