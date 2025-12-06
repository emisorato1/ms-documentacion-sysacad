# Informe de Pruebas de Carga - Servicio de Documentación

**Fecha:** Diciembre 2024  
**Servicio:** `ms-documentacion-sysacad`  
**Endpoint:** `GET /api/v1/certificado/{id}/pdf`  
**Herramienta:** Vegeta

---

## Resumen Ejecutivo

Se realizaron cinco ejecuciones de prueba de carga para evaluar el rendimiento del servicio de generación de certificados PDF bajo diferentes niveles de concurrencia. Los resultados muestran que el servicio opera de manera estable hasta **25 peticiones por segundo**, pero experimenta degradación significativa y errores 503 (Service Unavailable) al alcanzar **50 peticiones por segundo**. Las múltiples ejecuciones a 50 req/s muestran variabilidad en los resultados, confirmando la inestabilidad del sistema bajo esta carga.

---

## Escenarios de Prueba

### Escenario 1: Carga Baja (10 req/s)

**Comando ejecutado:**
```bash
vegeta attack -rate=10 -duration=30s -targets=./test_carga.txt | vegeta report
```

**Configuración:**
- Tasa de ataque: 10 peticiones/segundo
- Duración: 30 segundos
- Total de peticiones: 300

**Resultados:**
- ✅ **Tasa de éxito:** 100.00%
- **Throughput:** 9.97 req/s
- **Latencia media:** 262 ms
- **Latencia p50:** 218 ms
- **Latencia p99:** 823 ms
- **Latencia máxima:** 927 ms
- **Status Codes:** 200:300
- **Errores:** 0

**Evaluación:** 🟢 **EXCELENTE**  
El servicio maneja perfectamente esta carga. Los tiempos de respuesta son rápidos y consistentes, proporcionando una excelente experiencia de usuario.

---

### Escenario 2: Carga Media (25 req/s)

**Comando ejecutado:**
```bash
vegeta attack -rate=25 -duration=30s -targets=./test_carga.txt | vegeta report
```

**Configuración:**
- Tasa de ataque: 25 peticiones/segundo
- Duración: 30 segundos
- Total de peticiones: 750

**Resultados:**
- ✅ **Tasa de éxito:** 100.00%
- **Throughput:** 17.02 req/s
- **Latencia media:** 6.29 s
- **Latencia p50:** 5.46 s
- **Latencia p99:** 14.83 s
- **Latencia máxima:** 15.3 s
- **Status Codes:** 200:750
- **Errores:** 0

**Evaluación:** 🟡 **ACEPTABLE CON RESERVAS**  
Aunque todas las peticiones se completan exitosamente, se observa un aumento significativo en los tiempos de respuesta. El throughput real (17.02 req/s) es menor que la tasa solicitada (25 req/s), indicando que el sistema está cerca de su límite de capacidad.

---

### Escenario 3: Carga Alta (50 req/s) - Ejecución 1

**Comando ejecutado:**
```bash
vegeta attack -rate=50 -duration=30s -targets=./test_carga.txt | vegeta report
```

**Configuración:**
- Tasa de ataque: 50 peticiones/segundo
- Duración: 30 segundos
- Total de peticiones: 1500

**Resultados:**
- ❌ **Tasa de éxito:** 47.33%
- **Throughput:** 17.97 req/s
- **Latencia media:** 6.04 s
- **Latencia p50:** 7.8 ms
- **Latencia p99:** 24.37 s
- **Latencia máxima:** 25.54 s
- **Status Codes:** 200:710, 503:790
- **Errores:** 790 (503 Service Unavailable)

**Evaluación:** 🔴 **CRÍTICO**  
El servicio no puede manejar esta carga. Más de la mitad de las peticiones (52.67%) fallan con código 503 (Service Unavailable), indicando saturación del servidor o problemas de recursos. El throughput efectivo (17.97 req/s) es muy inferior a la demanda solicitada.

---

### Escenario 3: Carga Alta (50 req/s) - Ejecución 2

**Comando ejecutado:**
```bash
vegeta attack -rate=50 -duration=30s -targets=./test_carga.txt | vegeta report
```

**Configuración:**
- Tasa de ataque: 50 peticiones/segundo
- Duración: 30 segundos
- Total de peticiones: 1500

**Resultados:**
- ❌ **Tasa de éxito:** 49.27%
- **Throughput:** 12.79 req/s
- **Latencia media:** 20.82 s
- **Latencia p50:** 25.51 s
- **Latencia p99:** 30.00 s
- **Latencia máxima:** 30.01 s
- **Status Codes:** 0:651, 200:739, 503:110
- **Errores:** 
  - 651 timeouts (context deadline exceeded)
  - 110 errores 503 (Service Unavailable)

**Evaluación:** 🔴 **CRÍTICO - PEOR RENDIMIENTO**  
Esta ejecución muestra un rendimiento aún peor que la primera. El throughput cae a 12.79 req/s y se observan 651 timeouts, indicando que el sistema está completamente saturado y no puede responder dentro del tiempo límite del cliente.

---

### Escenario 3: Carga Alta (50 req/s) - Ejecución 3

**Comando ejecutado:**
```bash
vegeta attack -rate=50 -duration=30s -targets=./test_carga.txt | vegeta report
```

**Configuración:**
- Tasa de ataque: 50 peticiones/segundo
- Duración: 30 segundos
- Total de peticiones: 1500

**Resultados:**
- ❌ **Tasa de éxito:** 41.13%
- **Throughput:** 10.29 req/s
- **Latencia media:** 6.99 s
- **Latencia p50:** 5.80 ms
- **Latencia p99:** 30.00 s
- **Latencia máxima:** 30.00 s
- **Status Codes:** 0:58, 200:617, 503:825
- **Errores:**
  - 58 timeouts (context deadline exceeded)
  - 825 errores 503 (Service Unavailable)

**Evaluación:** 🔴 **CRÍTICO - MÁXIMA DEGRADACIÓN**  
Esta es la peor ejecución registrada. Solo el 41.13% de las peticiones son exitosas, con un throughput de apenas 10.29 req/s. Se observan 825 errores 503, la mayor cantidad registrada, confirmando la incapacidad del sistema para manejar esta carga.

---

## Análisis Comparativo

### Resumen por Escenario

| Escenario | Tasa de Éxito | Throughput | Latencia Media | Errores 503 | Timeouts | Estado |
|-----------|---------------|------------|----------------|-------------|----------|--------|
| **10 req/s** | 100% ✅ | 9.97 req/s | 262 ms | 0 | 0 | 🟢 Estable |
| **25 req/s** | 100% ✅ | 17.02 req/s | 6.29 s | 0 | 0 | 🟡 Límite |
| **50 req/s - Ejec 1** | 47.33% ❌ | 17.97 req/s | 6.04 s | 790 | 0 | 🔴 Saturado |
| **50 req/s - Ejec 2** | 49.27% ❌ | 12.79 req/s | 20.82 s | 110 | 651 | 🔴 Crítico |
| **50 req/s - Ejec 3** | 41.13% ❌ | 10.29 req/s | 6.99 s | 825 | 58 | 🔴 Crítico |






# Conclusión y Recomendaciones de Mejora


## 1. Conclusión Final del Rendimiento

Las pruebas de carga con Vegeta revelan que el servicio tiene un **límite operativo estricto ("Hard Cap") de aproximadamente 17-18 peticiones por segundo (req/s)**.

* **Rendimiento Óptimo (0-10 req/s):** El servicio responde en tiempos excelentes (~260ms), operando dentro de su zona de confort.
* **Punto de Saturación (25 req/s):** Se alcanza el límite de procesamiento. Aunque no hay errores, la latencia se dispara drásticamente (de ms a >6s), indicando saturación de CPU por la generación de PDFs.
* **Colapso del Sistema (50 req/s):** El servicio se vuelve inestable con una tasa de error superior al 50% (Service Unavailable y Timeouts). El throughput efectivo no supera las 18 req/s independientemente de la carga entrante.

**Diagnóstico:** El servicio sufre de un cuello de botella computacional (CPU-bound) inherente a la generación síncrona de documentos PDF.

---

## 2. Recomendaciones de Mejora

Se proponen las siguientes acciones priorizadas para estabilizar y escalar el servicio:

### 🔴 Prioridad Alta (Corto Plazo - Estabilidad)

1.  **Implementar Caché (Redis):**
    * *Acción:* Almacenar los PDFs generados en Redis con un TTL (tiempo de vida). Antes de generar, consultar si el archivo ya existe.
    * *Impacto:* Reducción drástica del uso de CPU y latencia inmediata para peticiones repetitivas.
2.  **Rate Limiting (Traefik):**
    * *Acción:* Configurar un middleware en el Gateway para limitar las peticiones a un máximo seguro (ej. 20 req/s).
    * *Impacto:* Evita la degradación del servicio y el colapso por saturación, devolviendo `429 Too Many Requests` en lugar de `503`.

### 🟡 Prioridad Media (Escalabilidad)

3.  **Escalado Horizontal:**
    * *Acción:* Desplegar al menos **3 réplicas** del microservicio balanceadas con Traefik.
    * *Impacto:* Aumentará el throughput linealmente (ej. de 17 req/s a ~50 req/s efectivos).

### 🟢 Prioridad Baja (Arquitectura Ideal - Largo Plazo)

4.  **Procesamiento Asíncrono (Colas):**
    * *Acción:* Desacoplar la petición HTTP de la generación del PDF usando una cola de mensajes (RabbitMQ/Redis) y workers en segundo plano.
    * *Impacto:* Elimina el bloqueo del servidor web, permitiendo manejar picos de miles de peticiones sin timeouts, notificando al usuario cuando su documento esté listo.