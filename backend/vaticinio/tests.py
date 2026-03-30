from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Pronostico

class PronosticoModelTest(TestCase):
    """Pruebas para el modelo Pronostico"""
    
    def setUp(self):
        self.pronostico = Pronostico.objects.create(
            fk_id_usuario=1,
            fk_id_partido=1,
            fk_id_liga=1,
            gol_local=2,
            gol_visitante=1
        )
    
    def test_creacion_pronostico(self):
        """Test que verifica la creación de un pronóstico"""
        self.assertEqual(self.pronostico.fk_id_usuario, 1)
        self.assertEqual(self.pronostico.fk_id_partido, 1)
        self.assertEqual(self.pronostico.fk_id_liga, 1)
        self.assertEqual(self.pronostico.gol_local, 2)
        self.assertEqual(self.pronostico.gol_visitante, 1)
    
    def test_str_pronostico(self):
        """Test que verifica el método __str__ del modelo"""
        expected = "Pronóstico {}: Usuario {} - Partido {} ({}-{})".format(
            self.pronostico.id_pronostico,
            self.pronostico.fk_id_usuario,
            self.pronostico.fk_id_partido,
            self.pronostico.gol_local,
            self.pronostico.gol_visitante
        )
        self.assertEqual(str(self.pronostico), expected)
    
    def test_resultado_display(self):
        """Test que verifica el resultado formateado"""
        self.assertEqual(self.pronostico.resultado_display, "2 - 1")
    
    def test_ganador_pronostico(self):
        """Test que verifica la determinación del ganador"""
        self.assertEqual(self.pronostico.ganador_pronostico, 'local')
        
        # Test empate
        self.pronostico.gol_local = 1
        self.pronostico.gol_visitante = 1
        self.assertEqual(self.pronostico.ganador_pronostico, 'empate')
        
        # Test visitante
        self.pronostico.gol_local = 0
        self.pronostico.gol_visitante = 2
        self.assertEqual(self.pronostico.ganador_pronostico, 'visitante')

class PronosticoAPITest(TestCase):
    """Pruebas para la API de Pronósticos"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.pronostico = Pronostico.objects.create(
            fk_id_usuario=1,
            fk_id_partido=1,
            fk_id_liga=1,
            gol_local=1,
            gol_visitante=1
        )
    
    def test_get_pronosticos_list(self):
        """Test para obtener la lista de pronósticos"""
        url = '/api/pronosticos/api/pronosticos/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_pronostico_detail(self):
        """Test para obtener un pronóstico específico"""
        url = f'/api/pronosticos/api/pronosticos/{self.pronostico.id_pronostico}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['fk_id_usuario'], 1)
        self.assertEqual(response.data['fk_id_partido'], 1)
    
    def test_create_pronostico(self):
        """Test para crear un nuevo pronóstico"""
        url = '/api/pronosticos/api/pronosticos/'
        data = {
            'fk_id_usuario': 2,
            'fk_id_partido': 2,
            'fk_id_liga': 1,
            'gol_local': 3,
            'gol_visitante': 2
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pronostico.objects.count(), 2)
    
    def test_duplicate_pronostico(self):
        """Test que previene pronósticos duplicados"""
        url = '/api/pronosticos/api/pronosticos/'
        data = {
            'fk_id_usuario': 1,  # Mismo usuario
            'fk_id_partido': 1,  # Mismo partido
            'fk_id_liga': 1,     # Misma liga
            'gol_local': 1,
            'gol_visitante': 0
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Ya existe un pronóstico', response.data['error'])
    
    def test_update_pronostico(self):
        """Test para actualizar un pronóstico existente"""
        url = f'/api/pronosticos/api/pronosticos/{self.pronostico.id_pronostico}/'
        data = {
            'gol_local': 3,
            'gol_visitante': 1
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.pronostico.refresh_from_db()
        self.assertEqual(self.pronostico.gol_local, 3)
        self.assertEqual(self.pronostico.gol_visitante, 1)
    
    def test_delete_pronostico(self):
        """Test para eliminar un pronóstico"""
        url = f'/api/pronosticos/api/pronosticos/{self.pronostico.id_pronostico}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Pronostico.objects.count(), 0)
    
    def test_validation_goles_negativos(self):
        """Test que previene goles negativos"""
        url = '/api/pronosticos/api/pronosticos/'
        data = {
            'fk_id_usuario': 3,
            'fk_id_partido': 3,
            'fk_id_liga': 1,
            'gol_local': -1,  # Gol negativo inválido
            'gol_visitante': 0
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_pronosticos_por_usuario(self):
        """Test para obtener pronósticos por usuario"""
        url = '/api/pronosticos/api/pronosticos/por-usuario/?usuario_id=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_pronosticos_por_liga(self):
        """Test para obtener pronósticos por liga"""
        url = '/api/pronosticos/api/pronosticos/por-liga/?liga_id=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_verificar_disponible(self):
        """Test para verificar disponibilidad de pronóstico"""
        url = '/api/pronosticos/api/pronosticos/verificar-disponible/'
        data = {
            'usuario_id': 1,
            'partido_id': 1,
            'liga_id': 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['disponible'])
        self.assertIn('Ya existe un pronóstico', response.data['mensaje'])
