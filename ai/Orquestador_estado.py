from game.campaign import SALAS
from game.characters import PERSONAJES


PROMPT_ORQUESTADOR = """
Eres un analizador de estado para un RPG.

Tu tarea NO es narrar.

Debes leer una narración y extraer únicamente:

- daño
- curación
- objetos ganados
- objetos perdidos
- cambios de ubicación
- eventos
- diálogos
- finales

Devuelve exclusivamente un JSON válido.
Nunca escribas explicaciones.
Nunca escribas texto fuera del JSON.
"""

def construir_contexto_orquestador(narracion):

    return f"""
Tipos de cambio permitidos:
danio
curacion
gana_objeto
pierde_objeto
cambiar_ubicacion
evento
cambiar_estado_personaje

Ubicaciones permitidas:
{SALAS}

Personajes permitidos:
{list(PERSONAJES.keys())}

Narracion:
{narracion}
"""

