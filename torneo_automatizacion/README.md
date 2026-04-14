# 🏆 Sistema de Automatización de Torneos Deportivos

Aplicación Python que automatiza la inserción masiva de equipos, jugadores y generación de calendarios de partidos utilizando **LangGraph** para la orquestación de workflows.

## 🚀 Características Principales

### 1. **Inserción Masiva de Equipos**
- Validación automática de datos con Pydantic
- Procesamiento por lotes de múltiples equipos
- Detección y reporte de errores individuales

### 2. **Inserción Masiva de Jugadores**
- Validación de posiciones (portero, defensa, centrocampista, delantero)
- Verificación de pertenencia a equipos existentes
- Asignación automática de IDs únicos

### 3. **Generación Óptima de Calendario**
- **Algoritmo Round-Robin** para distribución equilibrada
- Calendario de ida y vuelta automático
- Distribución inteligente de horarios y estadios
- Evita conflictos de localía

## 📁 Estructura del Proyecto

```
torneo_automatizacion/
├── main.py                 # Punto de entrada principal
├── models.py               # Modelos Pydantic (Equipo, Jugador, Partido)
├── agents.py               # Definición del estado para LangGraph
├── graph_workflow.py       # Workflow de automatización con LangGraph
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Este archivo
```

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**
- **LangGraph**: Orquestación de workflows con grafos de estado
- **Pydantic**: Validación y modelado de datos
- **Algoritmo Round-Robin**: Generación óptima de calendarios deportivos

## 📦 Instalación

```bash
cd torneo_automatizacion
pip install -r requirements.txt
```

## ▶️ Uso

### Ejecución Básica (con datos de ejemplo)

```bash
python main.py
```

Esto ejecutará:
1. Generación de 8 equipos de ejemplo
2. Inserción de 88 jugadores (11 por equipo)
3. Generación de 56 partidos (14 jornadas ida y vuelta)

### Personalizar Datos

Puedes modificar los datos de entrada en `main.py`:

```python
from graph_workflow import TournamentAutomationWorkflow

workflow = TournamentAutomationWorkflow()

# Tus propios datos
mis_datos = {
    "equipos": [
        {
            "nombre": "Mi Equipo FC",
            "ciudad": "Mi Ciudad",
            "fundacion": 2000,
            "estadio": "Mi Estadio",
            "entrenador": "Nombre Entrenador"
        },
        # ... más equipos
    ],
    "jugadores": [
        {
            "nombre": "Juan Pérez",
            "fecha_nacimiento": "1995-05-15",
            "posicion": "delantero",
            "numero_camiseta": 9,
            "equipo_id": 1,
            "nacionalidad": "España"
        },
        # ... más jugadores
    ]
}

resultado = workflow.ejecutar_automatizacion(mis_datos)
```

## 📊 Output Generado

La aplicación genera un archivo JSON `resultados_automatizacion.json` con:

```json
{
  "equipos": [...],
  "jugadores": [...],
  "partidos": [...],
  "resumen": {
    "total_equipos": 8,
    "total_jugadores": 88,
    "total_partidos": 56,
    "errores": 0
  }
}
```

## 🔍 Workflow de Ejecución

El sistema utiliza LangGraph para orquestar el siguiente flujo:

```
┌─────────────────────┐
│   Inicio Workflow   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Procesar Equipos   │ ◄── Validación masiva
└──────────┬──────────┘
           │
           ▼
     ¿Hay equipos?
      /         \
    Sí          No
     │            \
     ▼             \
┌─────────────────────┐  \
│ Procesar Jugadores  │   \──► Fin
└──────────┬──────────┘
           │
           ▼
  ¿Equipos y Jugadores?
      /         \
    Sí          No
     │            \
     ▼             \
┌─────────────────────┐  \
│ Generar Partidos    │   \──► Fin
│  (Round-Robin)      │
└──────────┬──────────┘
           │
           ▼
        Fin
```

## 🎯 Algoritmo Round-Robin

Para la generación de partidos se utiliza el algoritmo **Round-Robin** que garantiza:

- ✅ Cada equipo juega contra todos los demás
- ✅ Distribución equilibrada de localías (ida y vuelta)
- ✅ Máximo de 2 partidos por equipo por jornada
- ✅ Optimización de horarios y estadios

**Fórmula:**
- Para `n` equipos (par): `(n-1) × 2` jornadas
- Partidos por jornada: `n / 2`
- Total de partidos: `n × (n-1)`

Ejemplo con 8 equipos:
- 14 jornadas (7 ida + 7 vuelta)
- 4 partidos por jornada
- 56 partidos totales

## ⚙️ Validaciones Implementadas

### Equipos
- Campos requeridos: nombre, ciudad, fundación, estadio, entrenador
- Limpieza automática de espacios en blanco
- Conversión de tipos (año de fundación a entero)

### Jugadores
- Campos requeridos completos
- Posición válida (portero, defensa, centrocampista, delantero)
- Equipo ID existente en la base de datos
- Número de camiseta válido

### Partidos
- Mínimo 2 equipos requeridos
- No hay conflictos de localía
- Fechas distribuidas uniformemente

## 📝 Ejemplo de Salida

```
============================================================
🚀 INICIANDO AUTOMATIZACIÓN DE TORNEO DEPORTIVO
============================================================

🔵 Procesando equipos...
  ✓ Equipo validado: FC Madrid
  ✓ Equipo validado: Real Barcelona
  ...
✅ Equipos procesados: 8/8

🟢 Procesando jugadores...
  ✓ Jugador validado: Carlos García (portero)
  ...
✅ Jugadores procesados: 88/88

🟠 Generando calendario de partidos...
✅ Partidos generados: 56
   Jornadas: 14
   Partidos por jornada: 4

============================================================
📊 RESUMEN DE EJECUCIÓN
============================================================
Equipos insertados: 8
Jugadores insertados: 88
Partidos generados: 56
============================================================
✅ AUTOMATIZACIÓN COMPLETADA
```

## 🔧 Extensiones Futuras

Posibles mejoras:
- [ ] Integración con base de datos real (PostgreSQL, MySQL)
- [ ] API REST para integración con otros sistemas
- [ ] Interfaz web para carga de datos
- [ ] Exportación a formatos adicionales (CSV, Excel)
- [ ] Gestión de lesiones y suspensiones
- [ ] Estadísticas y reportes avanzados
- [ ] Integración con APIs de resultados en vivo

## 📄 Licencia

Este proyecto es de código abierto y puede ser modificado según necesidades.

## 👨‍💻 Autor

Desarrollado como solución de automatización para gestión de torneos deportivos.
