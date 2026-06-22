from django.test import TestCase
from django.urls import reverse
from .models import Producto

class ProductoModelTest(TestCase):
    def setUp(self):
        Producto.objects.create(nombre="Test Producto", descripcion="Test Desc", precio=10.50)

    def test_nombre_contenido(self):
        producto = Producto.objects.get(id=1)
        expected_object_name = f'{producto.nombre}'
        self.assertEqual(expected_object_name, 'Test Producto')

class ProductoViewTest(TestCase):
    def setUp(self):
        Producto.objects.create(nombre="Test Producto View", descripcion="View Desc", precio=20.00)

    def test_view_url_exists_at_proper_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_by_name(self):
        # ERROR INTENCIONAL PARA CAPTURA DE GITHUB ACTIONS
        self.assertEqual(1, 2)
        resp = self.client.get(reverse('producto_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'core/producto_list.html')
