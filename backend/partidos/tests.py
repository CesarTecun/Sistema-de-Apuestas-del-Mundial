from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Partido

class PartidoModelTest(TestCase):
    """Pruebas para el modelo Partido"""
    
    def setUp(self):
        self.partido = Partido.objects.create(
            horario='2026-06-15 14:00:00',
            equipo_local=1,
            equipo_visitante=2,
            fk_sede=1,
            fk_id_fase=1,
            gol_local=2,
            gol_visitante=1,
            ganador_penales=None,
            tipo_partido='Regular',
            resultado='Local 2-1 Visitante'
        )
    
    def test_creacion_partido(self):
        """Test que verifica la creación de un partido"""
        self.assertEqual(self.partido.equipo_local, 1)
        self.assertEqual(self.partido.equipo_visitante, 2)
        self.assertEqual(self.partido.gol_local, 2)
        self.assertEqual(self.partido.gol_visitante, 1)
        self.assertEqual(self.partido.tipo_partido, 'Regular')
    
    def test_str_partido(self):
        """Test que verifica el método __str__ del modelo"""
        expected = "Partido {}: {} vs {}".format(
            self.partido.id_partido, 
            self.partido.equipo_local, 
            self.partido.equipo_visitante
        )
        self.assertEqual(str(self.partido), expected)
    
    def test_resultado_display(self):
        """Test que verifica el resultado formateado"""
        self.assertEqual(self.partido.resultado_display, "2 - 1")
    
    def test_ganador(self):
        """Test que verifica la determinación del ganador"""
        self.assertEqual(self.partido.ganador, 1)  # Equipo local ganó

class PartidoAPITest(TestCase):
    """Pruebas para la API de Partidos"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.partido = Partido.objects.create(
            horario='2026-06-20 18:00:00',
            equipo_local=3,
            equipo_visitante=4,
            fk_sede=2,
            fk_id_fase=2,
            gol_local=0,
            gol_visitante=0,
            tipo_partido='Regular'
        )
    
    def test_get_partidos_list(self):
        """Test para obtener la lista de partidos"""
        url = '/api/partidos/api/partidos/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_partido_detail(self):
        """Test para obtener un partido específico"""
        url = f'/api/partidos/api/partidos/{self.partido.id_partido}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['equipo_local'], 3)
        self.assertEqual(response.data['equipo_visitante'], 4)
    
    def test_create_partido(self):
        """Test para crear un nuevo partido"""
        url = '/api/partidos/api/partidos/'
        data = {
            'horario': '2026-06-25 16:00:00',
            'equipo_local': 5,
            'equipo_visitante': 6,
            'fk_sede': 3,
            'fk_id_fase': 3,
            'gol_local': 0,
            'gol_visitante': 0,
            'tipo_partido': 'Regular'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Partido.objects.count(), 2)
    
    def test_update_partido(self):
        """Test para actualizar un partido existente"""
        url = f'/api/partidos/api/partidos/{self.partido.id_partido}/'
        data = {
            'gol_local': 3,
            'gol_visitante': 2,
            'resultado': 'Local 3-2 Visitante'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.partido.refresh_from_db()
        self.assertEqual(self.partido.gol_local, 3)
        self.assertEqual(self.partido.gol_visitante, 2)
    
    def test_delete_partido(self):
        """Test para eliminar un partido"""
        url = f'/api/partidos/api/partidos/{self.partido.id_partido}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Partido.objects.count(), 0)
    
    def test_actualizar_resultado(self):
        """Test para actualizar resultado de un partido"""
        url = f'/api/partidos/api/partidos/{self.partido.id_partido}/actualizar-resultado/'
        data = {
            'gol_local': 4,
            'gol_visitante': 2,
            'resultado': 'Local 4-2 Visitante'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.partido.refresh_from_db()
        self.assertEqual(self.partido.gol_local, 4)
        self.assertEqual(self.partido.resultado, 'Local 4-2 Visitante')
    
    def test_validation_goles_negativos(self):
        """Test que previene goles negativos"""
        url = '/api/partidos/api/partidos/'
        data = {
            'horario': '2026-06-30 15:00:00',
            'equipo_local': 7,
            'equipo_visitante': 8,
            'gol_local': -1,  # Gol negativo inválido
            'gol_visitante': 0,
            'tipo_partido': 'Regular'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
