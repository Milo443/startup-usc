from django.test import TestCase, Client
from django.urls import reverse
from .models import Proyecto, Financiero, CargoEmpleado
from django.db.models import Sum, F



#-------------TEST--------------------------------------------------------
class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_url = reverse('list')
        self.create_url = reverse('create')
        self.proyecto = Proyecto.objects.create(
            nombre='Proyecto1',
            descripcion='Descripcion1',
            categoria='Categoria1'
        )
        self.financiero = Financiero.objects.create(
            proyecto=self.proyecto,
            ventas=1000,
            costos_produccion=500,
            gastos_administrativos=200,
            capital_propio=100,
            prestamo=100,
            inversores=100
        )
        self.cargoempleado = CargoEmpleado.objects.create(
            nombre='Cargo1',
            salario=1000
        )

    def test_proyecto_list_GET(self):
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'emprendimiento/proyecto_list.html')

    def test_proyecto_create_GET(self):
        response = self.client.get(self.create_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'emprendimiento/proyecto_form.html')

    def test_proyecto_create_POST(self):
        response = self.client.post(self.create_url, {
            'nombre': 'Proyecto2',
            'descripcion': 'Descripcion2',
            'categoria': 'Categoria2'
        })
        proyecto = Proyecto.objects.get(id=2)
        self.assertEquals(proyecto.nombre, 'Proyecto2')
        self.assertEquals(proyecto.descripcion, 'Descripcion2')
        self.assertEquals(proyecto.categoria, 'Categoria2')

    def test_proyecto_update_POST(self):
        response = self.client.post(reverse('update', args='1'), {
            'nombre': 'Proyecto2',
            'descripcion': 'Descripcion2',
            'categoria': 'Categoria2'
        })
        proyecto = Proyecto.objects.get(id=1)
        self.assertEquals(proyecto.nombre, 'Proyecto2')
        self.assertEquals(proyecto.descripcion, 'Descripcion2')
        self.assertEquals(proyecto.categoria, 'Categoria2')

    def test_proyecto_delete_POST(self):
        response = self.client.post(reverse('delete', args='1'))
        proyectos = Proyecto.objects.all()
        self.assertEquals(len(proyectos), 0)

    def test_financiero_list_GET(self):
        response = self.client.get(reverse('financiero', args='1'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'emprendimiento/financiero_list.html')
    
    def test_financiero_create_POST(self):
        response = self.client.post(reverse('financiero', args='1'), {
            'ventas': 1000,
            'costos_produccion': 500,
            'gastos_administrativos': 200,
            'capital_propio': 100,
            'prestamo': 100,
            'inversores': 100
        })
        financiero = Financiero.objects.get(id=1)
        self.assertEquals(financiero.ventas, 1000)
        self.assertEquals(financiero.costos_produccion, 500)
        self.assertEquals(financiero.gastos_administrativos, 200)
        self.assertEquals(financiero.capital_propio, 100)
        self.assertEquals(financiero.prestamo, 100)
        self.assertEquals(financiero.inversores, 100)