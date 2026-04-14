from langgraph.graph import StateGraph, END
from agents import AgentState
from models import Equipo, Jugador, Partido, LoteEquipos, LoteJugadores, CalendarioPartidos
from typing import List
import json
from datetime import datetime, timedelta
import random

class TournamentAutomationWorkflow:
    """Workflow de automatización para gestión de torneos deportivos"""
    
    def __init__(self):
        self.equipos_db = []
        self.jugadores_db = []
        self.partidos_db = []
        
    def validar_y_procesar_equipos(self, state: AgentState) -> AgentState:
        """Valida y procesa equipos de forma masiva"""
        print("\n🔵 Procesando equipos...")
        input_data = state.get("input_data", {})
        equipos_raw = input_data.get("equipos", [])
        
        equipos_procesados = []
        errores = []
        
        for idx, equipo_data in enumerate(equipos_raw):
            try:
                # Validación básica
                if not all(k in equipo_data for k in ["nombre", "ciudad", "fundacion", "estadio", "entrenador"]):
                    raise ValueError(f"Equipo {idx+1}: Faltan campos requeridos")
                
                equipo = Equipo(
                    id=len(self.equipos_db) + len(equipos_procesados) + 1,
                    nombre=equipo_data["nombre"].strip(),
                    ciudad=equipo_data["ciudad"].strip(),
                    fundacion=int(equipo_data["fundacion"]),
                    estadio=equipo_data["estadio"].strip(),
                    entrenador=equipo_data["entrenador"].strip()
                )
                equipos_procesados.append(equipo.dict())
                print(f"  ✓ Equipo validado: {equipo.nombre}")
            except Exception as e:
                error_msg = f"Error en equipo {idx+1}: {str(e)}"
                errores.append(error_msg)
                print(f"  ✗ {error_msg}")
        
        state["equipos_procesados"] = equipos_procesados
        state["errores"] = state.get("errores", []) + errores
        state["paso_actual"] = "equipos_completados"
        
        print(f"✅ Equipos procesados: {len(equipos_procesados)}/{len(equipos_raw)}")
        return state
    
    def validar_y_procesar_jugadores(self, state: AgentState) -> AgentState:
        """Valida y procesa jugadores de forma masiva"""
        print("\n🟢 Procesando jugadores...")
        input_data = state.get("input_data", {})
        jugadores_raw = input_data.get("jugadores", [])
        equipos_ids = [e["id"] for e in state.get("equipos_procesados", [])]
        
        jugadores_procesados = []
        errores = []
        posiciones_validas = ["portero", "defensa", "centrocampista", "delantero"]
        
        for idx, jugador_data in enumerate(jugadores_raw):
            try:
                # Validaciones
                if not all(k in jugador_data for k in ["nombre", "fecha_nacimiento", "posicion", "numero_camiseta", "equipo_id", "nacionalidad"]):
                    raise ValueError(f"Jugador {idx+1}: Faltan campos requeridos")
                
                if jugador_data["equipo_id"] not in equipos_ids:
                    raise ValueError(f"Jugador {idx+1}: Equipo ID no válido")
                
                posicion = jugador_data["posicion"].lower().strip()
                if posicion not in posiciones_validas:
                    raise ValueError(f"Jugador {idx+1}: Posición no válida. Debe ser: {', '.join(posiciones_validas)}")
                
                jugador = Jugador(
                    id=len(self.jugadores_db) + len(jugadores_procesados) + 1,
                    nombre=jugador_data["nombre"].strip(),
                    fecha_nacimiento=jugador_data["fecha_nacimiento"].strip(),
                    posicion=posicion,
                    numero_camiseta=int(jugador_data["numero_camiseta"]),
                    equipo_id=int(jugador_data["equipo_id"]),
                    nacionalidad=jugador_data["nacionalidad"].strip()
                )
                jugadores_procesados.append(jugador.dict())
                print(f"  ✓ Jugador validado: {jugador.nombre} ({jugador.posicion})")
            except Exception as e:
                error_msg = f"Error en jugador {idx+1}: {str(e)}"
                errores.append(error_msg)
                print(f"  ✗ {error_msg}")
        
        state["jugadores_procesados"] = jugadores_procesados
        state["errores"] = state.get("errores", []) + errores
        state["paso_actual"] = "jugadores_completados"
        
        print(f"✅ Jugadores procesados: {len(jugadores_procesados)}/{len(jugadores_raw)}")
        return state
    
    def generar_calendario_partidos(self, state: AgentState) -> AgentState:
        """Genera automáticamente el calendario de partidos optimizado"""
        print("\n🟠 Generando calendario de partidos...")
        equipos = state.get("equipos_procesados", [])
        
        if len(equipos) < 2:
            state["errores"] = state.get("errores", []) + ["Se necesitan al menos 2 equipos para generar partidos"]
            state["partidos_generados"] = []
            return state
        
        # Algoritmo round-robin para distribución óptima
        n_equipos = len(equipos)
        jornadas_totales = (n_equipos - 1) * 2  # Ida y vuelta
        partidos_por_jornada = n_equipos // 2
        
        # Crear lista rotativa para el algoritmo round-robin
        indices = list(range(n_equipos))
        partidos_generados = []
        fecha_base = datetime.now() + timedelta(days=7)
        
        for jornada in range(1, jornadas_totales + 1):
            for i in range(partidos_por_jornada):
                local_idx = indices[i]
                visitante_idx = indices[n_equipos - 1 - i]
                
                # En jornada de vuelta, intercambiar localía
                if jornada > n_equipos - 1:
                    local_idx, visitante_idx = visitante_idx, local_idx
                
                equipo_local = equipos[local_idx]
                equipo_visitante = equipos[visitante_idx]
                
                # Distribuir horarios de forma óptima
                hora_offset = (jornada - 1) * 2 + i
                fecha_partido = fecha_base + timedelta(weeks=jornada-1, hours=hora_offset % 24)
                
                partido = Partido(
                    id=len(self.partidos_db) + len(partidos_generados) + 1,
                    equipo_local_id=equipo_local["id"],
                    equipo_visitante_id=equipo_visitante["id"],
                    fecha=fecha_partido.strftime("%Y-%m-%d %H:%M"),
                    estadio=equipo_local["estadio"],
                    jornada=jornada if jornada <= n_equipos - 1 else jornada - (n_equipos - 1),
                    estado="programado"
                )
                partidos_generados.append(partido.dict())
            
            # Rotar índices para siguiente jornada (manteniendo primero fijo)
            indices = [indices[0]] + [indices[-1]] + indices[1:-1]
        
        state["partidos_generados"] = partidos_generados
        state["paso_actual"] = "calendario_generado"
        
        print(f"✅ Partidos generados: {len(partidos_generados)}")
        print(f"   Jornadas: {jornadas_totales}")
        print(f"   Partidos por jornada: {partidos_por_jornada}")
        
        return state
    
    def should_continue_to_jugadores(self, state: AgentState) -> str:
        """Decide si continuar al procesamiento de jugadores"""
        if state.get("equipos_procesados"):
            return "procesar_jugadores"
        return "fin"
    
    def should_continue_to_partidos(self, state: AgentState) -> str:
        """Decide si continuar a la generación de partidos"""
        if state.get("jugadores_procesados") is not None and state.get("equipos_procesados"):
            return "generar_partidos"
        return "fin"
    
    def construir_workflow(self):
        """Construye el grafo de workflow con LangGraph"""
        workflow = StateGraph(AgentState)
        
        # Añadir nodos
        workflow.add_node("procesar_equipos", self.validar_y_procesar_equipos)
        workflow.add_node("procesar_jugadores", self.validar_y_procesar_jugadores)
        workflow.add_node("generar_partidos", self.generar_calendario_partidos)
        
        # Definir flujo
        workflow.set_entry_point("procesar_equipos")
        
        # Condición después de procesar equipos
        workflow.add_conditional_edges(
            "procesar_equipos",
            self.should_continue_to_jugadores,
            {
                "procesar_jugadores": "procesar_jugadores",
                "fin": END
            }
        )
        
        # Condición después de procesar jugadores
        workflow.add_conditional_edges(
            "procesar_jugadores",
            self.should_continue_to_partidos,
            {
                "generar_partidos": "generar_partidos",
                "fin": END
            }
        )
        
        workflow.add_edge("generar_partidos", END)
        
        return workflow.compile()
    
    def ejecutar_automatizacion(self, datos_entrada: dict) -> dict:
        """Ejecuta todo el proceso de automatización"""
        print("="*60)
        print("🚀 INICIANDO AUTOMATIZACIÓN DE TORNEO DEPORTIVO")
        print("="*60)
        
        workflow = self.construir_workflow()
        
        estado_inicial = {
            "messages": [],
            "input_data": datos_entrada,
            "equipos_procesados": [],
            "jugadores_procesados": [],
            "partidos_generados": [],
            "errores": [],
            "paso_actual": "inicio"
        }
        
        resultado = workflow.invoke(estado_inicial)
        
        print("\n" + "="*60)
        print("📊 RESUMEN DE EJECUCIÓN")
        print("="*60)
        print(f"Equipos insertados: {len(resultado['equipos_procesados'])}")
        print(f"Jugadores insertados: {len(resultado['jugadores_procesados'])}")
        print(f"Partidos generados: {len(resultado['partidos_generados'])}")
        
        if resultado['errores']:
            print(f"\n⚠️ Errores encontrados: {len(resultado['errores'])}")
            for error in resultado['errores'][:5]:  # Mostrar primeros 5 errores
                print(f"  - {error}")
        
        print("="*60)
        print("✅ AUTOMATIZACIÓN COMPLETADA")
        print("="*60)
        
        return resultado


# Función helper para generar datos de ejemplo
def generar_datos_ejemplo(n_equipos=8, n_jugadores_por_equipo=11):
    """Genera datos de ejemplo para testing"""
    ciudades = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao", "Zaragoza", "Málaga", "Murcia"]
    nombres_equipos = ["FC", "Real", "Atlético", "Deportivo", "Sporting", "Racing", "Unión", "Club"]
    apellidos = ["García", "Rodríguez", "Martínez", "López", "González", "Sánchez", "Pérez", "Fernández"]
    nombres = ["Carlos", "David", "Juan", "Pedro", "Luis", "Miguel", "Antonio", "José"]
    posiciones = ["portero", "defensa", "centrocampista", "delantero"]
    nacionalidades = ["España", "Argentina", "Brasil", "México", "Colombia", "Chile", "Uruguay", "Portugal"]
    
    equipos = []
    for i in range(n_equipos):
        equipo = {
            "nombre": f"{nombres_equipos[i]} {ciudades[i]}",
            "ciudad": ciudades[i],
            "fundacion": 1900 + i * 5,
            "estadio": f"Estadio {ciudades[i]}",
            "entrenador": f"Entrenador {apellidos[i]}"
        }
        equipos.append(equipo)
    
    jugadores = []
    jugador_id = 1
    for equipo_idx, equipo in enumerate(equipos):
        equipo_id = equipo_idx + 1
        for j in range(n_jugadores_por_equipo):
            jugador = {
                "nombre": f"{nombres[j % len(nombres)]} {apellidos[(j + equipo_idx) % len(apellidos)]}",
                "fecha_nacimiento": f"{1990 + (j % 10)}-{(j % 12) + 1:02d}-{(j % 28) + 1:02d}",
                "posicion": posiciones[j % len(posiciones)],
                "numero_camiseta": (j % 99) + 1,
                "equipo_id": equipo_id,
                "nacionalidad": nacionalidades[(j + equipo_idx) % len(nacionalidades)]
            }
            jugadores.append(jugador)
    
    return {"equipos": equipos, "jugadores": jugadores}