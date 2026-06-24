# test_gemini.py

from ai.GeminiClient import GeminiClient

gemini = GeminiClient()

print(
    gemini.generar_texto(
        "Di hola"
    )
)