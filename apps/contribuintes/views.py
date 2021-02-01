from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Contribuinte
from .forms import ContribuinteForm

from apps.tesouraria.models import LancamentoOferta


class CreateContribuinte(LoginRequiredMixin, CreateView):
    template_name = 'create_contribuinte.html'
    form_class = ContribuinteForm
    extra_context = {}

    def form_valid(self, form):
        success_url = HttpResponseRedirect(reverse_lazy("contribuintes:contribuintes"))
        if not self.request.is_ajax():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
            success_url = HttpResponseRedirect(self.get_success_url())
        else:
            pass
        return success_url

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(CreateContribuinte, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs


class ContribuinteDetailView(LoginRequiredMixin, DetailView):
    template_name = 'detalhes_contribuinte.html'
    extra_context = {}

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Contribuinte.objects.filter(user=self.request.user)
        else:
            return Contribuinte.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contribuicoes'] = self.request.user.lancamentooferta.filter(contribuinte=self.kwargs.get('pk'))
        return context


class ContribuinteListView(LoginRequiredMixin, ListView):
    template_name = 'lista_contribuintes.html'
    context_object_name = 'contribuintes'
    paginate_by = 10
    ordering = ['-created']
    extra_context = {}

    def get_queryset(self):
        return Contribuinte.objects.filter(user=self.request.user)


class UpdateContribuinte(LoginRequiredMixin, UpdateView):
    template_name = 'atualiza_contribuinte.html'
    model = Contribuinte
    fields = ['nome', 'data_nasc']
    success_url = reverse_lazy('contribuintes:contribuintes')


class DeleteContribuinte(LoginRequiredMixin, DeleteView):
    template_name = 'confirmar_deletar_contribuinte.html'
    model = Contribuinte
    success_url = reverse_lazy('contribuintes:contribuintes')
