from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Producto
from .forms import ProductoForm

class ProductoListView(ListView):
    model = Producto
    template_name = 'core/producto_list.html'
    context_object_name = 'productos'
    ordering = ['-fecha_creacion']

class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'core/producto_form.html'
    success_url = reverse_lazy('producto_list')

class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'core/producto_form.html'
    success_url = reverse_lazy('producto_list')

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'core/producto_confirm_delete.html'
    success_url = reverse_lazy('producto_list')
