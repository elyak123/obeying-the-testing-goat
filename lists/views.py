from django.shortcuts import render, reverse
from django.http      import HttpResponse
from django.shortcuts import render, redirect
from lists.models     import Item
# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def view_list(request):
    #import pdb; pdb.set_trace()
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})

def new_list(request):
    if request.POST:
        Item.objects.create(text=request.POST['item_text'])
        url = reverse('view_list')
        return redirect(url)
    else:
        return HttpResponse('bla')
