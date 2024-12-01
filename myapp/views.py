from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import DeleteView

from .models import Consume, Food

# Create your views here.


class Index(ListView):
    model = Food
    template_name = 'myapp/index.html'
    context_object_name = 'food_list'


    def post(self, request, *args, **kwargs):
        food_consumed = request.POST.get('food_consumed')
        consume = Food.objects.get(name=food_consumed)
        user = request.user
        consume = Consume(user=user, food_consumed=consume)
        consume.save()
    
        return HttpResponseRedirect(reverse('index'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['consumed_items'] = Consume.objects.filter(user=self.request.user)
        return context
    

class ConsumeDelete(DeleteView):
    model = Consume
    template_name = 'myapp/consume_confirm_delete.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_all'] = False  # Not deleting all
        return context

class ConsumeDeleteAll(View):
    template_name = 'myapp/consume_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'delete_all': True}) 

    def post(self, request, *args, **kwargs):
        Consume.objects.filter(user=request.user).delete()
        return HttpResponseRedirect(reverse_lazy('index'))