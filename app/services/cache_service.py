import json
import redis
from flask import current_app
from app.mapping import EspecialidadMapping


class CacheService:
    _redis_client = None
    
    @staticmethod
    def _get_redis_client():
        """Crea y retorna un cliente de Redis configurado (reutiliza la conexión)"""
        if CacheService._redis_client is None:
            host = current_app.config.get('REDIS_HOST', 'localhost')
            port = int(current_app.config.get('REDIS_PORT', '6379'))
            password = current_app.config.get('REDIS_PASSWORD', '')
            
            CacheService._redis_client = redis.Redis(
                host=host,
                port=port,
                password=password if password else None,
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=2
            )
        return CacheService._redis_client
    
    @staticmethod
    def obtener_especialidad(id: int):
        """Intenta obtener la especialidad desde Redis. Retorna None si no existe"""
        try:
            client = CacheService._get_redis_client()
            clave = f'especialidad:{id}'
            datos = client.get(clave)
            
            if datos:
                datos_json = json.loads(datos)
                mapping = EspecialidadMapping()
                return mapping.load(datos_json)
            
            return None
        except Exception:
            # Si hay error al conectar o leer de Redis, retornar None
            return None

