import unittest
from app.mapping.alumno_mapping import AlumnoMapping
from app.mapping.especialidad_mapping import EspecialidadMapping


class AlumnoMappingTestCase(unittest.TestCase):

    def test_cargar_alumno_valido(self):
        """Test TDD: Verifica carga correcta de datos de alumno válidos"""
        mapping = AlumnoMapping()
        data = {
            'id': 1,
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'nro_documento': 12345678,
            'tipo_documento': 'DNI',
            'sexo': 'M',
            'nro_legajo': 1000,
            'especialidad_id': 1
        }
        
        alumno = mapping.load(data)
        
        self.assertIsNotNone(alumno)
        self.assertEqual(alumno.id, 1)
        self.assertEqual(alumno.nombre, 'Juan')
        self.assertEqual(alumno.apellido, 'Pérez')
        self.assertEqual(alumno.nrodocumento, '12345678')  # Convertido a string
        self.assertEqual(alumno.tipo_documento.sigla, 'DNI')
        self.assertEqual(alumno.especialidad_id, 1)

    def test_cargar_alumno_con_nro_documento_string(self):
        """Test TDD: Verifica conversión de nro_documento a string"""
        mapping = AlumnoMapping()
        data = {
            'id': 1,
            'nombre': 'María',
            'apellido': 'García',
            'nro_documento': 98765432,  # Como int
            'tipo_documento': 'Pasaporte',
            'sexo': 'F',
            'nro_legajo': 2000,
            'especialidad_id': 2
        }
        
        alumno = mapping.load(data)
        
        self.assertIsInstance(alumno.nrodocumento, str)
        self.assertEqual(alumno.nrodocumento, '98765432')

    def test_validar_campos_requeridos(self):
        """Test TDD: Verifica validación de campos requeridos"""
        mapping = AlumnoMapping()
        data_incompleto = {
            'id': 1,
            # Falta nombre y otros campos requeridos
        }
        
        with self.assertRaises(Exception):
            mapping.load(data_incompleto)

    def test_crear_tipo_documento_desde_string(self):
        """Test TDD: Verifica creación de TipoDocumento desde string"""
        tipo_doc = AlumnoMapping._crear_tipo_documento('DNI')
        
        self.assertIsNotNone(tipo_doc)
        self.assertEqual(tipo_doc.sigla, 'DNI')
        self.assertEqual(tipo_doc.nombre, 'DNI')
        self.assertEqual(tipo_doc.id, 1)


class EspecialidadMappingTestCase(unittest.TestCase):

    def test_cargar_especialidad_valida(self):
        """Test TDD: Verifica carga correcta de especialidad"""
        mapping = EspecialidadMapping()
        data = {
            'id': 1,
            'especialidad': 'Ingeniería en Sistemas',
            'facultad': 'FRBA',
            'universidad': 'UTN'
        }
        
        especialidad = mapping.load(data)
        
        self.assertIsNotNone(especialidad)
        self.assertEqual(especialidad.id, 1)
        self.assertEqual(especialidad.nombre, 'Ingeniería en Sistemas')  # Mapeado desde 'especialidad'
        self.assertEqual(especialidad.facultad, 'FRBA')
        self.assertEqual(especialidad.universidad, 'UTN')

    def test_cargar_especialidad_con_valores_por_defecto(self):
        """Test TDD: Verifica valores por defecto para campos opcionales"""
        mapping = EspecialidadMapping()
        data = {
            'id': 1,
            'especialidad': 'Ingeniería',
            'facultad': 'FRBA',
            'universidad': 'UTN'
            # Sin letra ni observacion
        }
        
        especialidad = mapping.load(data)
        
        self.assertEqual(especialidad.letra, '')
        self.assertIsNone(especialidad.observacion)


if __name__ == '__main__':
    unittest.main()

