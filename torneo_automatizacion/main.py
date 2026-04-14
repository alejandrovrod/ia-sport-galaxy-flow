#!/usr/bin/env python3
"""
Aplicación de Automatización para Gestión de Torneos Deportivos
Utiliza LangGraph para orquestar el workflow de inserción masiva de:
- Equipos
- Jugadores  
- Partidos (calendario optimizado con algoritmo round-robin)

Autor: Asistente de IA
"""

import sys
import json
from pathlib import Path

# Asegurar que el directorio actual esté en el path
sys.path.insert(0, str(Path(__file__).parent))

from graph_workflow import TournamentAutomationWorkflow, generar_datos_ejemplo


def main():
    """Función principal de la aplicación"""
    
    print("\n" + "="*60)
    print("⚽ SISTEMA DE AUTOMATIZACIÓN DE TORNEOS DEPORTIVOS ⚽")
    print("="*60)
    print("\nEsta aplicación automatiza la inserción masiva de:")
    print("  1. ✅ Equipos deportivos")
    print("  2. ✅ Jugadores por equipo")
    print("  3. ✅ Calendario de partidos (distribución óptima)")
    print("\nTecnologías utilizadas:")
    print("  • Python + Pydantic (validación de datos)")
    print("  • LangGraph (orquestación de workflows)")
    print("  • Algoritmo Round-Robin (generación de calendarios)")
    print("="*60)
    
    # Inicializar el workflow
    workflow = TournamentAutomationWorkflow()
    
    # Opción 1: Usar datos de ejemplo
    print("\n📋 Generando datos de ejemplo para demostración...")
    print("   - 8 equipos")
    print("   - 11 jugadores por equipo (88 total)")
    print("   - Calendario completo ida y vuelta")
    
    datos_ejemplo = generar_datos_ejemplo(n_equipos=8, n_jugadores_por_equipo=11)
    
    # Ejecutar la automatización
    resultado = workflow.ejecutar_automatizacion(datos_ejemplo)
    
    # Mostrar resultados detallados
    print("\n" + "="*60)
    print("📄 DETALLES DE RESULTADOS")
    print("="*60)
    
    # Mostrar primeros 3 equipos
    print("\n🔵 PRIMEROS EQUIPOS INSERTADOS:")
    for equipo in resultado['equipos_procesados'][:3]:
        print(f"   • {equipo['nombre']} ({equipo['ciudad']}) - Estadio: {equipo['estadio']}")
    if len(resultado['equipos_procesados']) > 3:
        print(f"   ... y {len(resultado['equipos_procesados']) - 3} equipos más")
    
    # Mostrar primeros 5 jugadores
    print("\n🟢 PRIMEROS JUGADORES INSERTADOS:")
    for jugador in resultado['jugadores_procesados'][:5]:
        print(f"   • {jugador['nombre']} - {jugador['posicion'].capitalize()} #{jugador['numero_camiseta']}")
    if len(resultado['jugadores_procesados']) > 5:
        print(f"   ... y {len(resultado['jugadores_procesados']) - 5} jugadores más")
    
    # Mostrar primeros 5 partidos
    print("\n🟠 PRIMEROS PARTIDOS GENERADOS:")
    equipos_dict = {e['id']: e['nombre'] for e in resultado['equipos_procesados']}
    for partido in resultado['partidos_generados'][:5]:
        local = equipos_dict.get(partido['equipo_local_id'], f"Equipo {partido['equipo_local_id']}")
        visitante = equipos_dict.get(partido['equipo_visitante_id'], f"Equipo {partido['equipo_visitante_id']}")
        print(f"   • Jornada {partido['jornada']}: {local} vs {visitante}")
        print(f"     📅 {partido['fecha']} | 🏟️ {partido['estadio']}")
    
    if len(resultado['partidos_generados']) > 5:
        print(f"   ... y {len(resultado['partidos_generados']) - 5} partidos más")
    
    # Guardar resultados en archivo JSON
    archivo_salida = Path(__file__).parent / "resultados_automatizacion.json"
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        json.dump({
            "equipos": resultado['equipos_procesados'],
            "jugadores": resultado['jugadores_procesados'],
            "partidos": resultado['partidos_generados'],
            "resumen": {
                "total_equipos": len(resultado['equipos_procesados']),
                "total_jugadores": len(resultado['jugadores_procesados']),
                "total_partidos": len(resultado['partidos_generados']),
                "errores": len(resultado['errores'])
            }
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados guardados en: {archivo_salida}")
    
    print("\n" + "="*60)
    print("✅ PROCESO COMPLETADO EXITOSAMENTE")
    print("="*60)
    
    return resultado


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Proceso interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)