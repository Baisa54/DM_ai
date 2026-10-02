from modelo.configuracion import ConfigManager

def obtener_cliente_texto():
    """
    Retorna la instancia del cliente de IA configurado para procesar texto, arbitraje de acciones,
    actualización de estado y diálogos en el pipeline cognitivo.
    
    Proveedores soportados:
    - 'ollama': Inferencia local offline con Llama 3.1 / modelos GGUF (por defecto).
    - 'openai' o 'chatgpt': Inferencia ultra-rápida en la nube con gpt-4o-mini (modo presentación CACIC).
    - 'gemini': Inferencia en la nube con Google Gemini API.
    """
    config = ConfigManager()
    proveedor = config.get_proveedor_texto().lower().strip()

    if proveedor in ("openai", "chatgpt"):
        from modelo.ai.OpenAIClient import OpenAIClient
        return OpenAIClient()
    elif proveedor == "gemini":
        from modelo.ai.GeminiClient import GeminiClient
        return GeminiClient()
    else:
        from modelo.ai.LocalAICLient import LocalAIClient
        return LocalAIClient()
