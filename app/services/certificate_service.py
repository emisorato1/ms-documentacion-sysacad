import datetime
import requests
from io import BytesIO
from flask import current_app
from app.mapping import AlumnoMapping, EspecialidadMapping
from app.models import Alumno
from app.services.documentos_office_service import obtener_tipo_documento

class CertificateService:
    @staticmethod
    def generar_certificado_alumno_regular(id: int, tipo: str) -> BytesIO:
        alumno = CertificateService._buscar_alumno_por_id(id)
        if not alumno:
            return None
        
        # Obtener especialidad usando el especialidad_id del alumno
        especialidad = CertificateService._buscar_especialidad_por_id(alumno.especialidad_id)
        if not especialidad:
            raise Exception(f'Error al obtener la especialidad con id {alumno.especialidad_id}')
        
        # Asignar la especialidad al alumno
        alumno.especialidad = especialidad
        
        context = CertificateService._obtener_contexto_alumno(alumno)
        documento = obtener_tipo_documento(tipo)
        if not documento:
            return None
            
        if tipo in ('odt', 'docx'):
            plantilla = 'certificado_plantilla'
        else:
            plantilla = 'certificado_pdf'

        return documento.generar(
            carpeta='certificado',
            plantilla=plantilla,
            context=context
        )
    
    @staticmethod
    def _obtener_contexto_alumno(alumno: Alumno) -> dict:
        especialidad = alumno.especialidad
        # Crear objetos simples para facultad y universidad que el template espera
        facultad = type('Facultad', (), {'nombre': especialidad.facultad})()
        universidad = type('Universidad', (), {'nombre': especialidad.universidad or 'Universidad'})()
        
        return {
            "alumno": alumno,
            "especialidad": especialidad,
            "facultad": facultad,
            "universidad": universidad,
            "fecha": CertificateService._obtener_fechaactual()
        }
    
    @staticmethod
    def _obtener_fechaactual() -> str:
        fecha_actual = datetime.datetime.now()
        fecha_str = fecha_actual.strftime('%d de %B de %Y')
        return fecha_str
    
    @staticmethod
    def _buscar_alumno_por_id(id: int) -> Alumno:
        alumnos_host = current_app.config.get('ALUMNOS_HOST', 'http://localhost:8080')
        url_alumnos = f'{alumnos_host}/api/v1/alumnos'
        alumno_mapping = AlumnoMapping()
        r = requests.get(f'{url_alumnos}/{id}')
        if r.status_code == 200:
            result = alumno_mapping.load(r.json())  
        else:
            raise Exception(f'Error al obtener el alumno con id {id}: {r.status_code}')
        return result
    
    @staticmethod
    def _buscar_especialidad_por_id(id: int):
        academica_host = current_app.config.get('ACADEMICA_HOST', 'http://localhost:8081')
        url_especialidades = f'{academica_host}/api/v1/especialidades'
        especialidad_mapping = EspecialidadMapping()
        r = requests.get(f'{url_especialidades}/{id}')
        if r.status_code == 200:
            result = especialidad_mapping.load(r.json())
        else:
            raise Exception(f'Error al obtener la especialidad con id {id}: {r.status_code}')
        return result
