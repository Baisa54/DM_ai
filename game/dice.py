import random

#------------------------------------------------------------------------------------------------------
# Dice
#
# La idea de dice es que tire el dado y calcule el resultado dependiendo la dificultad
#------------------------------------------------------------------------------------------------------

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