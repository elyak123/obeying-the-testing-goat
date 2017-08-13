from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http      import HttpResponse
from django.shortcuts import render, redirect
from lists.models     import Item, List
# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    if request.method == 'POST':
        item = Item(text=request.POST['item_text'], list=list_)
        try:
            item.full_clean()
        except ValidationError:
            error = "You can't have an empty list item"
            #item.delete()
            return render(request, 'list.html', {'list': list_ ,'error': error})
        item.save()
        return redirect(list_)
    return render(request, 'list.html', {'list': list_})

def new_list(request):
    if request.POST:
        list_ = List.objects.create()
        item = Item.objects.create(text=request.POST['item_text'], list=list_)
        try:
            item.full_clean()
        except ValidationError:
            error = "You can't have an empty list item"
            list_.delete()
            return render(request, 'home.html', {'error': error})
        list_.save()
        return redirect(list_)
