from django.core.exceptions import ValidationError
from django.views.generic   import FormView, CreateView, DetailView
from django.shortcuts import render
from django.http      import HttpResponse
from django.shortcuts import render, redirect
from lists.models     import Item, List
from lists.forms      import ItemForm, ExistingListItemForm
# Create your views here.
class HomePageView(FormView):
    template_name = 'home.html'
    form_class    = ItemForm

class ViewAndAddToList(DetailView, CreateView):
    model         = List
    template_name = 'list.html'
    form_class    = ExistingListItemForm

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, 'form': form})

class NewListView(CreateView):
    form_class = ItemForm
    template_name = 'home.html'

    def form_valid(self, form):
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)

def new_list(request):
    if request.POST:
        form = ItemForm(data=request.POST)
        if form.is_valid():
            list_ = List.objects.create()
            form.save(for_list=list_)
            return redirect(list_)
        else:
            return render(request, 'home.html', {'form': form})