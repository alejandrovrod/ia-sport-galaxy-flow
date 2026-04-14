from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Equipo(BaseModel):
    """Modelo para representar un equipo deportivo"""
    id: Optional[int] = None
    nombre: str = Field(..., description="Nombre del equipo")
    ciudad: str = Field(..., description="Ciudad del equipo")
    fundacion: int = Field(..., description="Año de fundación")
    estadio: str = Field(..., description="Nombre del estadio")
    entrenador: str = Field(..., description="Nombre del entrenador")

class Jugador(BaseModel):
    """Modelo para representar un jugador"""
    id: Optional[int] = None
    nombre: str = Field(..., description="Nombre completo del jugador")
    fecha_nacimiento: str = Field(..., description="Fecha de nacimiento (YYYY-MM-DD)")
    posicion: str = Field(..., description="Posición en el campo")
    numero_camiseta: int = Field(..., description="Número de camiseta")
    equipo_id: int = Field(..., description="ID del equipo al que pertenece")
    nacionalidad: str = Field(..., description="Nacionalidad del jugador")

class Partido(BaseModel):
    """Modelo para representar un partido"""
    id: Optional[int] = None
    equipo_local_id: int = Field(..., description="ID del equipo local")
    equipo_visitante_id: int = Field(..., description="ID del equipo visitante")
    fecha: str = Field(..., description="Fecha del partido (YYYY-MM-DD HH:MM)")
    estadio: str = Field(..., description="Estadio donde se juega")
    jornada: int = Field(..., description="Número de jornada")
    estado: str = Field(default="programado", description="Estado del partido")

class LoteEquipos(BaseModel):
    """Modelo para procesamiento masivo de equipos"""
    equipos: List[Equipo] = Field(..., description="Lista de equipos a insertar")

class LoteJugadores(BaseModel):
    """Modelo para procesamiento masivo de jugadores"""
    jugadores: List[Jugador] = Field(..., description="Lista de jugadores a insertar")

class CalendarioPartidos(BaseModel):
    """Modelo para generación de calendario de partidos"""
    partidos: List[Partido] = Field(..., description="Lista de partidos generados")