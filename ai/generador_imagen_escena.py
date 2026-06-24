PROMPT_IMAGEN_ESCENA = """
Eres un ilustrador de RPG.

Debes generar una ilustración que represente
la situación actual.

REGLAS:

- Usa los personajes de referencia.
- Respeta completamente su apariencia.
- No cambies vestimenta.
- No cambies raza.
- No cambies colores.

La escena debe representar exactamente
lo ocurrido en la narración.

Estilo:
Comic D&D.

No agregar texto.
No agregar UI.
No agregar globos de diálogo.

Imagen panorámica de aventura.
"""

def generar_imagen_escena(
    narracion,
    imagenes_personajes
):
    prompt = f"""
{PROMPT_IMAGEN_ESCENA}

NARRACION:

{narracion}
"""
    
    