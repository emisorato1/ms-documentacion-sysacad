import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from app import create_app
from app.services.certificate_service import CertificateService
from app.services.cache_service import CacheService
from app.models import Alumno, Especialidad, TipoDocumento
import os


class CertificateServiceTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_obtener_fechaactual_formato_correcto(self):
        """Test TDD: Verifica que _obtener_fechaactual retorna formato correcto"""
        fecha = CertificateService._obtener_fechaactual()
        # Debe tener formato "dd de Mes de yyyy" (ej: "15 de diciembre de 2024")
        self.assertIsInstance(fecha, str)
        self.assertIn('de', fecha)
        # Verificar que contiene números (día y año)
        self.assertTrue(any(c.isdigit() for c in fecha))

    def test_obtener_contexto_alumno_estructura_correcta(self):
        """Test TDD: Verifica que _obtener_contexto_alumno retorna estructura correcta"""
        # Crear objetos de prueba
        especialidad = Especialidad()
        especialidad.id = 1
        especialidad.nombre = "Ingeniería en Sistemas"
        especialidad.facultad = "Facultad Regional"
        especialidad.universidad = "UTN"
        especialidad.letra = ""
        especialidad.observacion = None
        
        tipo_doc = TipoDocumento()
        tipo_doc.id = 1
        tipo_doc.sigla = "DNI"
        tipo_doc.nombre = "DNI"
        
        alumno = Alumno()
        alumno.id = 1
        alumno.nombre = "Juan"
        alumno.apellido = "Pérez"
        alumno.nrodocumento = "12345678"
        alumno.tipo_documento = tipo_doc
        alumno.nro_legajo = 1000
        alumno.especialidad = especialidad
        
        contexto = CertificateService._obtener_contexto_alumno(alumno)
        
        # Verificar estructura del contexto
        self.assertIn('alumno', contexto)
        self.assertIn('especialidad', contexto)
        self.assertIn('facultad', contexto)
        self.assertIn('universidad', contexto)
        self.assertIn('fecha', contexto)
        
        # Verificar tipos y valores
        self.assertEqual(contexto['alumno'].id, alumno.id)
        self.assertEqual(contexto['especialidad'].nombre, especialidad.nombre)
        self.assertEqual(contexto['facultad'].nombre, especialidad.facultad)
        self.assertEqual(contexto['universidad'].nombre, especialidad.universidad)

    @patch('app.services.certificate_service.requests.get')
    def test_buscar_alumno_por_id_exitoso(self, mock_get):
        """Test TDD: Verifica búsqueda exitosa de alumno"""
        # Mock de respuesta exitosa
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 1,
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'nro_documento': 12345678,
            'tipo_documento': 'DNI',
            'sexo': 'M',
            'nro_legajo': 1000,
            'especialidad_id': 1
        }
        mock_get.return_value = mock_response
        
        alumno = CertificateService._buscar_alumno_por_id(1)
        
        self.assertIsNotNone(alumno)
        self.assertEqual(alumno.id, 1)
        self.assertEqual(alumno.nombre, 'Juan')
        self.assertEqual(alumno.apellido, 'Pérez')

    @patch('app.services.certificate_service.requests.get')
    def test_buscar_alumno_por_id_error(self, mock_get):
        """Test TDD: Verifica manejo de error al buscar alumno"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        with self.assertRaises(Exception) as context:
            CertificateService._buscar_alumno_por_id(999)
        
        self.assertIn('Error al obtener el alumno', str(context.exception))


class CacheServiceTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()
        # Limpiar cliente Redis estático
        CacheService._redis_client = None

    @patch('app.services.cache_service.redis.Redis')
    def test_obtener_especialidad_desde_cache(self, mock_redis_class):
        """Test TDD: Verifica obtención de especialidad desde Redis"""
        # Mock de Redis con datos
        mock_client = MagicMock()
        mock_client.get.return_value = '{"id": 1, "especialidad": "Ingeniería", "facultad": "FRBA", "universidad": "UTN"}'
        mock_redis_class.return_value = mock_client
        CacheService._redis_client = None  # Resetear para forzar nueva conexión
        
        especialidad = CacheService.obtener_especialidad(1)
        
        self.assertIsNotNone(especialidad)
        self.assertEqual(especialidad.id, 1)
        self.assertEqual(especialidad.nombre, "Ingeniería")
        mock_client.get.assert_called_once_with('especialidad:1')

    @patch('app.services.cache_service.redis.Redis')
    def test_obtener_especialidad_cache_vacio(self, mock_redis_class):
        """Test TDD: Verifica que retorna None cuando no hay datos en cache"""
        mock_client = MagicMock()
        mock_client.get.return_value = None
        mock_redis_class.return_value = mock_client
        CacheService._redis_client = None
        
        especialidad = CacheService.obtener_especialidad(999)
        
        self.assertIsNone(especialidad)

    @patch('app.services.cache_service.redis.Redis')
    def test_obtener_especialidad_error_redis(self, mock_redis_class):
        """Test TDD: Verifica manejo de errores de conexión a Redis"""
        # Simular error de conexión
        mock_redis_class.side_effect = Exception("Connection error")
        CacheService._redis_client = None
        
        # Debe retornar None sin lanzar excepción
        especialidad = CacheService.obtener_especialidad(1)
        self.assertIsNone(especialidad)


if __name__ == '__main__':
    unittest.main()

