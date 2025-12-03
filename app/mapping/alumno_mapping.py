from marshmallow import Schema, fields, post_load, validate
from app.models import Alumno, TipoDocumento

class AlumnoMapping(Schema):
    id = fields.Integer()
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=50))
    apellido = fields.String(required=True, validate=validate.Length(min=1, max=50))
    # El mock devuelve nro_documento como int, lo convertimos a string
    nro_documento = fields.Raw(required=True, data_key='nro_documento')
    # El mock devuelve tipo_documento como string (DNI, Pasaporte, LE)
    tipo_documento = fields.String(required=True, data_key='tipo_documento')
    sexo = fields.String(required=True, validate=validate.Length(equal=1))
    nro_legajo = fields.Integer(required=True, data_key='nro_legajo')
    especialidad_id = fields.Integer(required=True, data_key='especialidad_id')

    @post_load
    def nuevo_alumno(self, data, **kwargs):
        # Convertir nro_documento a string si viene como int
        if 'nro_documento' in data:
            data['nrodocumento'] = str(data.pop('nro_documento'))
        
        # Crear TipoDocumento a partir del string que viene del mock
        tipo_doc_str = data.pop('tipo_documento', 'DNI')
        tipo_documento = AlumnoMapping._crear_tipo_documento(tipo_doc_str)
        data['tipo_documento'] = tipo_documento
        
        # El modelo no tiene especialidad todavía, se asignará después
        # pero necesitamos guardar el especialidad_id temporalmente
        especialidad_id = data.pop('especialidad_id')
        
        # Crear el alumno sin especialidad primero
        alumno = Alumno()
        alumno.id = data.get('id')
        alumno.nombre = data.get('nombre')
        alumno.apellido = data.get('apellido')
        alumno.nrodocumento = data.get('nrodocumento')
        alumno.tipo_documento = data.get('tipo_documento')
        alumno.nro_legajo = data.get('nro_legajo', 0)
        # Guardar especialidad_id como atributo temporal
        alumno.especialidad_id = especialidad_id
        
        return alumno
    
    @staticmethod
    def _crear_tipo_documento(tipo_str: str) -> TipoDocumento:
        """Crea un TipoDocumento a partir de un string del mock"""
        tipo_doc = TipoDocumento()
        tipo_doc.id = 1  # Valor por defecto
        tipo_doc.sigla = tipo_str
        tipo_doc.nombre = tipo_str
        return tipo_doc
