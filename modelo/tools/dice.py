#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# dice
#
# dice provee funciones auxiliares para simular tiradas de dados d20 y verificar
# el éxito o fracaso de las mismas basándose en una dificultad predeterminada,
# considerando pifias (1) y éxitos críticos (20).
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# (No define elementos o constantes a nivel de módulo)
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
# 
# @ tirar_d20
#   --> Devuelve un número entero aleatorio entre 1 y 20.
# @ verificar_tirada, recibe el resultado de la tirada (int) y la dificultad (int)
#   --> Devuelve un diccionario con el resultado de la validación ("exito" y "tipo").
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
import random
# random se utiliza para la generación de números aleatorios para la tirada de dados
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

def tirar_d20():
    return random.randint(1, 20)

def verificar_tirada(resultado, dificultad):

    if resultado == 1:
        return {
            "exito": False,
            "tipo": "pifia"
        }

    if resultado == 20:
        return {
            "exito": True,
            "tipo": "critico"
        }

    return {
        "exito": resultado >= dificultad,
        "tipo": "normal",
    }