from typing import TypedDict, List, Annotated
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    """Estado compartido para el workflow de LangGraph"""
    messages: Annotated[List[BaseMessage], operator.add]
    input_data: dict
    equipos_procesados: List
    jugadores_procesados: List
    partidos_generados: List
    errores: List[str]
    paso_actual: str