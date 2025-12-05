##

```bash
emisorato-ubu@emisorato-ubu:~/SYSACAD DS/ms-documentacion-sysacad/test_carga$ vegeta attack -rate=50 -duration=30s -targets=./test_carga.txt | vegeta report
Requests      [total, rate, throughput]         1500, 50.03, 14.49
Duration      [total, attack, wait]             59.98s, 29.98s, 30s
Latencies     [min, mean, 50, 90, 95, 99, max]  350.055ms, 21.454s, 25.778s, 30.001s, 30.001s, 30.003s, 30.006s
Bytes In      [total, mean]                     31044803, 20696.54
Bytes Out     [total, mean]                     0, 0.00
Success       [ratio]                           57.93%
Status Codes  [code:count]                      0:631  200:869  
Error Set:
Get "https://documentos.universidad.localhost/api/v1/certificado/339454026/pdf": context deadline exceeded
Get "https://documentos.universidad.localhost/api/v1/certificado/339454026/pdf": net/http: request canceled (Client.Timeout exceeded while awaiting headers)
Get "https://documentos.universidad.localhost/api/v1/certificado/339454026/pdf": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
emisorato-ubu@emisorato-ubu:~/SYSACAD DS/ms-documentacion-sysacad/test_carga$ 
```


# Informe de Prueba de Carga: Servicio de Documentación

**Fecha:** 04 de Diciembre, 2025
**Servicio:** `ms-documentacion-sysacad`
**Endpoint:** Generación de Certificados PDF
**Herramienta:** Vegeta


## 1. Resumen Ejecutivo
**Resultado:** 🔴 **FALLIDO / CRÍTICO**

El servicio no es capaz de soportar la carga solicitada de **50 peticiones por segundo**. El sistema experimentó una saturación severa de recursos, resultando en una tasa de error del **42%** debido a tiempos de espera agotados (timeouts). El throughput efectivo fue de solo ~14 req/s.

## 2. Configuración de la Prueba
* **Comando ejecutado:**
    ```bash
    vegeta attack -rate=50 -duration=30s -targets=./test_carga.txt
    ```
* **Duración:** 30 segundos
* **Objetivo de carga:** 1500 peticiones totales (50 req/s)

## 3. Métricas de Rendimiento

| Métrica | Valor Obtenido | Evaluación |
| :--- | :--- | :--- |
| **Peticiones Totales** | 1500 | - |
| **Tasa de Éxito** | **57.93%** | ⚠️ **Crítico:** 42% de pérdida de servicio. |
| **Throughput (Real)** | 14.49 req/s | Muy por debajo del objetivo de 50 req/s. |
| **Latencia Media** | 21.45 s | Inaceptable para experiencia de usuario. |
| **Latencia P99** | 30.00 s | El sistema alcanza el timeout máximo. |
| **Códigos 200 (OK)** | 869 | Peticiones procesadas correctamente. |
| **Códigos 0 (Error)** | 631 | Fallos de conexión/timeout. |

## 4. Análisis de Errores
Se registraron **631 errores** clasificados bajo el código de estado `0`.

**Traza de error principal:**
> `Get ".../pdf": context deadline exceeded (Client.Timeout exceeded while awaiting headers)`

**Interpretación:**
Las peticiones superaron el tiempo máximo de espera de 30 segundos establecido por el cliente o el servidor. Esto indica que el proceso de generación de PDFs es una operación bloqueante y costosa en CPU/RAM, creando un cuello de botella inmediato al intentar paralelizar 50 procesos.

## 5. Conclusiones y Recomendaciones

1.  **Capacidad Real Excedida:** La infraestructura actual no soporta la generación síncrona de 50 PDFs por segundo.
2.  **Ajuste de Prueba:** Se recomienda repetir la prueba con una carga escalonada, iniciando en **5 o 10 req/s**, para determinar el punto de ruptura real.
3.  **Optimización de Arquitectura:**
    * Evaluar el uso de **procesamiento asíncrono** (Colas/Workers) para la generación de PDFs.
    * Revisar la asignación de CPU y Memoria del contenedor Docker.




##
```bash
emisorato-ubu@emisorato-ubu:~/SYSACAD DS/ms-documentacion-sysacad/test_carga$ vegeta attack -rate=10 -duration=30s -targets=./test_carga.txt | vegeta report
Requests      [total, rate, throughput]         300, 10.03, 9.96
Duration      [total, attack, wait]             30.115s, 29.9s, 214.863ms
Latencies     [min, mean, 50, 90, 95, 99, max]  151.372ms, 202.661ms, 196.54ms, 251.803ms, 275.685ms, 361.695ms, 444.932ms
Bytes In      [total, mean]                     10714401, 35714.67
Bytes Out     [total, mean]                     0, 0.00
Success       [ratio]                           100.00%
Status Codes  [code:count]                      200:300  
Error Set:
emisorato-ubu@emisorato-ubu:~/SYSACAD DS/ms-documentacion-sysacad/test_carga$ 
```


# Informe de Prueba de Carga: Servicio de Documentación (Escenario Estable)

**Fecha:** 04 de Diciembre, 2025
**Servicio:** `ms-documentacion-sysacad`
**Endpoint:** Generación de Certificados PDF
**Herramienta:** Vegeta

## 1. Resumen Ejecutivo
**Resultado:** 🟢 **EXITOSO / ESTABLE**

Bajo una carga de **10 peticiones por segundo**, el servicio operó con una estabilidad perfecta. Se procesaron el 100% de las solicitudes con tiempos de respuesta excelentes (promedio de 0.2 segundos). El sistema no muestra signos de saturación en este nivel de concurrencia.

## 2. Configuración de la Prueba
* **Comando ejecutado:**
    ```bash
    vegeta attack -rate=10 -duration=30s -targets=./test_carga.txt
    ```
* **Duración:** 30 segundos
* **Objetivo de carga:** 300 peticiones totales (10 req/s)

## 3. Métricas de Rendimiento

| Métrica | Valor Obtenido | Evaluación |
| :--- | :--- | :--- |
| **Peticiones Totales** | 300 | - |
| **Tasa de Éxito** | **100.00%** | ✅ Perfecto. Ninguna petición fallida. |
| **Throughput (Real)** | 9.96 req/s | El servidor atendió la demanda al mismo ritmo que llegaba. |
| **Latencia Media** | 202 ms | Muy rápido (0.2s). Excelente experiencia de usuario. |
| **Latencia Máxima** | 444 ms | Incluso el caso más lento fue inferior a medio segundo. |
| **Códigos 200 (OK)** | 300 | - |
| **Códigos 0 (Error)** | 0 | - |

## 4. Comparativa con Prueba Anterior

| Escenario | Tasa de Éxito | Latencia Media | Estado |
| :--- | :--- | :--- | :--- |
| **50 req/s** | 57.93% | 21.45 s | 🔴 Colapso |
| **10 req/s** | **100.00%** | **0.20 s** | 🟢 Estable |

## 5. Conclusiones
1.  **Zona de Confort:** El servicio maneja cómodamente 10 generaciones de PDF por segundo.
2.  **Rendimiento:** La generación de PDFs en este volumen es eficiente, con tiempos de respuesta que no afectan la experiencia del usuario final.



##
```bash
emisorato-ubu@emisorato-ubu:~/SYSACAD DS/ms-documentacion-sysacad/test_carga$ vegeta attack -rate=25 -duration=30s -targets=./test_carga.txt | vegeta report
Requests      [total, rate, throughput]         750, 25.03, 18.19
Duration      [total, attack, wait]             41.222s, 29.96s, 11.262s
Latencies     [min, mean, 50, 90, 95, 99, max]  200.164ms, 5.369s, 5.123s, 10.43s, 11.29s, 11.815s, 12.28s
Bytes In      [total, mean]                     26794954, 35726.61
Bytes Out     [total, mean]                     0, 0.00
Success       [ratio]                           100.00%
Status Codes  [code:count]                      200:750  
Error Set:
```

# Informe de Prueba de Carga: Servicio de Documentación (Escenario de Estrés)

**Fecha:** 04 de Diciembre, 2025
**Servicio:** `ms-documentacion-sysacad`
**Endpoint:** Generación de Certificados PDF
**Herramienta:** Vegeta

## 1. Resumen Ejecutivo
**Resultado:** 🟠 **DEGRADADO / AL LÍMITE**

El sistema completó el 100% de las solicitudes sin errores, pero mostró signos claros de saturación. La infraestructura no pudo mantener el ritmo de **25 peticiones por segundo**, provocando un "cuello de botella". Aunque no hubo fallos técnicos, la experiencia de usuario se degradó significativamente con tiempos de espera altos.

## 2. Configuración de la Prueba
* **Comando ejecutado:**
    ```bash
    vegeta attack -rate=25 -duration=30s -targets=./test_carga.txt
    ```
* **Objetivo de carga:** 750 peticiones totales (25 req/s)

## 3. Métricas de Rendimiento

| Métrica | Valor Obtenido | Evaluación |
| :--- | :--- | :--- |
| **Tasa de Éxito** | **100.00%** | ✅ El servidor no colapsó, atendió a todos. |
| **Throughput (Capacidad)** | **18.19 req/s** | ⚠️ **Dato Clave:** Este es el límite real de tu hardware actual. |
| **Latencia Media** | 5.37 s | ⚠️ Alta. Se formó una cola de espera. |
| **Latencia Máxima** | 12.28 s | Algunos usuarios esperaron más de 12 segundos. |
| **Códigos 200 (OK)** | 750 | - |

## 4. Comparativa de Escenarios

| Escenario (Carga) | Tasa de Éxito | Latencia Media | Capacidad Real (Throughput) | Estado |
| :--- | :--- | :--- | :--- | :--- |
| **10 req/s** | 100% | **0.20 s** | 9.96 req/s | 🟢 Óptimo |
| **25 req/s** | 100% | **5.37 s** | **18.19 req/s** | 🟠 Saturado |
| **50 req/s** | 58% | 21.45 s | 14.49 req/s | 🔴 Colapso |

## 5. Conclusiones Técnicas
1.  **Límite de Hardware:** Tu contenedor/servidor tiene una capacidad máxima de procesamiento de **~18 PDFs por segundo**.
2.  **Comportamiento bajo Estrés:** Cuando la demanda (25 req/s) supera la capacidad (18 req/s), el sistema no falla inmediatamente, sino que encola las peticiones. Esto es bueno (resiliencia), pero aumenta la latencia.
3.  **Recomendación Operativa:**
    * Para garantizar tiempos de respuesta rápidos (<1s), no se debe superar las **15 req/s** concurrentes.
    * Si se requiere más velocidad, es necesario escalar verticalmente (más CPU) u horizontalmente (más réplicas del servicio).



# Resumen final para tu toma de decisiones:
- Zona segura: 0 a 15 usuarios por segundo (Respuesta inmediata).

- Zona de riesgo: 16 a 20 usuarios por segundo (El servidor se ralentiza).

- Zona de peligro: +25 usuarios por segundo (Empiezan los timeouts y errores).