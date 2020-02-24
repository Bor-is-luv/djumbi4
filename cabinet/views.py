from django.shortcuts import render
from .models import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CreateGroup


def cabinet_view(request):
    context = {}
    template = 'cabinet.html'
    context['groups'] = Group.objects.get(user=request.user)
    return render(request, template, context)


class CreateGroupView(CreateView):
    model = Group
    template_name = 'create_group.html'
    form_class = CreateGroup
    success_url = reverse_lazy('cabinet_page')

    def form_valid(self, form):
        self.object = form.save()
        self.object.teacher = self.request.user
        self.object.save()
        return super().form_valid(form)
