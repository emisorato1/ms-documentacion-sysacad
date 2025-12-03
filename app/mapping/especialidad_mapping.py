from marshmallow import fields, Schema, post_load, validate
from app.models import Especialidad


class EspecialidadMapping(Schema):
    id = fields.Integer()
    # El mock devuelve "especialidad" como nombre
    especialidad = fields.String(required=True, validate=validate.Length(min=1, max=100), data_key='especialidad')
    facultad = fields.String(required=True)
    universidad = fields.String(required=True)
    
    # Campos opcionales para compatibilidad
    letra = fields.String(validate=validate.Length(equal=1), allow_none=True, load_default='')
    observacion = fields.String(validate=validate.Length(max=255), allow_none=True, load_default=None)

    @post_load
    def nueva_especialidad(self, data, **kwargs):
        # Mapear "especialidad" a "nombre" para el modelo
        if 'especialidad' in data:
            data['nombre'] = data.pop('especialidad')
        # Asegurar que letra y observacion tengan valores por defecto si no vienen
        if 'letra' not in data:
            data['letra'] = ''
        if 'observacion' not in data:
            data['observacion'] = None
        
        # Crear la instancia de Especialidad asignando atributos directamente
        especialidad = Especialidad()
        especialidad.id = data.get('id')
        especialidad.nombre = data.get('nombre', '')
        especialidad.letra = data.get('letra', '')
        especialidad.observacion = data.get('observacion')
        especialidad.facultad = data.get('facultad', '')
        especialidad.universidad = data.get('universidad')
        
        return especialidad