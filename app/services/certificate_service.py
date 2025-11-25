import datetime
import os
import requests
from io import BytesIO
from types import SimpleNamespace
from app.mapping import AlumnoMapping
from app.models import Alumno
from app.services.documentos_office_service import obtener_tipo_documento

class CertificateService:
    @staticmethod
    def generar_certificado_alumno_regular(id: int, tipo: str) -> BytesIO:
        alumno = CertificateService._buscar_alumno_por_id(id)
        if not alumno:
            return None
        
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
        facultad = especialidad.facultad
        universidad = facultad.universidad
        return {
            "alumno": alumno,
            "especialidad": especialidad,
            "facultad": facultad,
            "universidad": universidad,
            "fecha": CertificateService._obtener_fechaactual()
        }
    
    @staticmethod
    def _obtener_fechaactual():
        fecha_actual = datetime.datetime.now()
        fecha_str = fecha_actual.strftime('%d de %B de %Y')
        return fecha_str
    
    @staticmethod
    def _buscar_alumno_por_id(id: int) -> Alumno:
        # Obtener URLs desde variables de entorno (pueden apuntar a los mocks)
        URL_ALUMNOS = os.getenv('ALUMNO_SERVICE_URL', 'http://mock-alumno:8080/api/v1/alumnos')
        URL_ESPECIALIDADES = os.getenv('GESTION_SERVICE_URL', 'http://mock-gestion:8080/api/v1/especialidades')

        # Llamada al servicio de alumnos
        r = requests.get(f'{URL_ALUMNOS}/{id}')
        if r.status_code != 200:
            raise Exception(f'Error al obtener el alumno con id {id}: {r.status_code}')
        alumno_json = r.json()

        # Extraer especialidad_id desde la respuesta del mock (compatibilidad con varios nombres)
        especialidad_id = alumno_json.get('especialidad_id') or alumno_json.get('especialidadId') or alumno_json.get('especialidad')
        if especialidad_id is None:
            raise Exception(f'No se encontró especialidad_id en la respuesta del alumno: {alumno_json}')

        # Llamada al servicio de gestion (especialidades)
        r2 = requests.get(f'{URL_ESPECIALIDADES}/{especialidad_id}')
        if r2.status_code != 200:
            raise Exception(f'Error al obtener la especialidad con id {especialidad_id}: {r2.status_code}')
        especialidad_json = r2.json()

        # Construir objetos simples que cumplan con la estructura mínima esperada
        facultad_obj = SimpleNamespace(
            nombre=especialidad_json.get('facultad') or especialidad_json.get('Facultad'),
            universidad=especialidad_json.get('universidad') or especialidad_json.get('Universidad')
        )

        especialidad_obj = SimpleNamespace(
            id=especialidad_json.get('id'),
            nombre=especialidad_json.get('especialidad') or especialidad_json.get('Especialidad'),
            facultad=facultad_obj
        )

        tipo_doc_val = alumno_json.get('tipo_documento') or alumno_json.get('tipoDocumento') or alumno_json.get('tipo')
        tipo_doc_obj = SimpleNamespace(sigla=tipo_doc_val, nombre=tipo_doc_val)

        alumno_obj = SimpleNamespace(
            id=alumno_json.get('id'),
            nombre=alumno_json.get('nombre'),
            apellido=alumno_json.get('apellido'),
            nrodocumento=str(alumno_json.get('nro_documento') or alumno_json.get('nrodocumento') or ''),
            tipo_documento=tipo_doc_obj,
            especialidad=especialidad_obj
        )

        return alumno_obj
    
