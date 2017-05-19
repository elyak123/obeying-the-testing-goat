from django.shortcuts import render, reverse
from django.http      import HttpResponse
from django.shortcuts import render, redirect
from lists.models     import Item, List
# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def view_list(request):
    #import pdb; pdb.set_trace()
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})

def new_list(request):
    if request.POST:
        list_ = List.objects.create()
        Item.objects.create(text=request.POST['item_text'], list=list_)
        url = reverse('view_list')
        return redirect(url)
    else:
        return HttpResponse('bla')
