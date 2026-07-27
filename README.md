# DM-ai

## ¿Por qué DM-ai y qué propongo?
DM-ai es un prototipo de Director de Juego (DM) basado en inteligencia artificial, diseñado para ofrecer una experiencia de rol narrativo inspirada en Dungeons and Dragons. 

Los juegos de rol clásicos ofrecen una libertad de acción inigualable. Si bien videojuegos como *Baldur's Gate 3* logran capturar parte de esta magia, siguen limitados por un conjunto finito de acciones y caminos predefinidos. Por otro lado, aunque los modelos de lenguaje actuales permiten generar historias dinámicas (como en FableAI), carecen de mecanismos formales para resolver acciones puntuales (como una tirada de d20) y les cuesta mantener un estado coherente y persistente del mundo a lo largo de una campaña. A esto se le suma la dificultad habitual de coordinar los horarios de varios jugadores para mantener partidas presenciales.

Frente a estas limitaciones, propongo DM-ai: un sistema capaz de administrar el estado de la partida, interpretar las acciones del jugador y resolver sus consecuencias mediante un sistema basado en reglas y tiradas de dados. Mi objetivo es lograr una narración interactiva consistente, utilizando estructuras JSON para coordinar la comunicación interna, y modelos de lenguaje (tanto locales como en la nube, según se prefiera) para dar vida a una verdadera experiencia de rol sin las restricciones de las historias pre-programadas.

## Requisitos antes de jugar
Para poder ejecutar el juego en tu computadora, especialmente si lo haces por primera vez, necesitas tener instalados dos programas fundamentales. Los archivos ejecutables del juego (como `Jugar_Windows.bat` o `Jugar_Linux.sh`) están preparados para facilitarte el resto del proceso.

### 1. Python
El juego está programado en Python, por lo que es necesario tenerlo instalado en tu sistema.
* **Descarga:** Puedes descargarlo de forma gratuita desde su página oficial: [python.org/downloads](https://www.python.org/downloads/).
* **⚠️ Instalación en Windows:** Es **crítico** que, al iniciar el instalador de Python, te asegures de marcar la casilla inferior que dice **"Add Python to PATH"** (Agregar Python al PATH). Si omites este paso, los archivos ejecutables no podrán detectar Python y el juego no abrirá.
* **Librerías (Pygame):** Aunque los ejecutables del juego intentan instalar todas las dependencias por ti, si tienes algún problema al abrirlo, te recomendamos abrir una terminal (o Símbolo del Sistema) y ejecutar manualmente: `pip install pygame` (o `pip install -r requirements.txt`).

### 2. Ollama
Ollama es el motor que permite ejecutar modelos de Inteligencia Artificial de forma local en tu computadora, lo cual es necesario para la generación de la historia del juego.
* **Descarga e Instalación:** Descárgalo desde su web oficial: [ollama.com/download](https://ollama.com/download).
* **Uso:** Instálalo y asegúrate de abrir el programa para que quede activo en tu computadora. Debe estar ejecutándose en segundo plano para que el juego pueda generar el texto y comunicarse con la IA.
* **Recomendación de Modelo:** Te recomendamos descargar el modelo **Llama 3.1**, ya que es el que estamos utilizando por defecto para este proyecto. Una vez instalado Ollama, abre una terminal o símbolo del sistema y ejecuta el comando `ollama run llama3.1` para descargarlo automáticamente.

### ¿Cómo iniciar el juego?
Una vez que tengas **Python** y **Ollama** instalados, ve a la carpeta del juego y ejecuta el archivo correspondiente a tu sistema operativo (por ejemplo, `Jugar_Windows.bat` si usas Windows).
La primera vez que lo ejecutes, el script detectará que te faltan las librerías del juego (como Pygame) y te preguntará: `¿Deseas crear el entorno virtual e instalar las dependencias de Python? (s/n):`.
Escribe **`s`** y presiona Enter. El script creará un entorno seguro (entorno virtual) e instalará todo lo necesario de forma completamente automática, para luego iniciar el juego.

## Herramientas Elegidas
Para el desarrollo de DM-ai he seleccionado un conjunto de tecnologías robustas y eficientes que permiten construir todo el sistema, desde la lógica hasta la interfaz gráfica interactiva:
- **Python**: Como lenguaje de programación principal, gracias a su inmenso ecosistema de librerías para IA y su facilidad para un desarrollo rápido.
- **Pygame**: Utilizado para construir toda la Vista (interfaz gráfica de usuario). Al ser un proyecto inspirado en videojuegos y juegos de rol, Pygame me permite manejar los eventos de ventana, renderizado de texto interactivo y controles visuales con mayor libertad que las librerías GUI tradicionales.
- **google-genai**: La librería oficial para integrar el modelo de Google Gemini directamente al proyecto. A través del cliente `GeminiClient`, esta librería maneja las solicitudes complejas hacia la IA en la nube.
- **huggingface-hub**: Para facilitar la interacción y posible descarga de modelos abiertos alojados en Hugging Face, sirviendo como un pilar importante para la inferencia local.
- **requests**: Una herramienta indispensable para realizar peticiones HTTP. La utilizo para la comunicación en red con las APIs y para el cliente `LocalAIClient`, permitiendo el paso de JSON de un lado a otro.
- **Pillow (PIL)**: Librería para el procesamiento de imágenes. Se utiliza en conjunto con la vista para manejar recursos gráficos, escalar imágenes o adaptar texturas necesarias dentro del renderizado de Pygame.
- **pyperclip**: Implementado para aportar usabilidad al sistema, permitiendo que el jugador o el DM puedan interactuar con el portapapeles (copiar/pegar) de manera fluida directamente desde la interfaz gráfica.
- **JSON**: La librería estándar de Python para el manejo y persistencia de la configuración del sistema (`config.json`), logrando que parámetros clave (como qué IA usar, u otros datos de entorno) sean fácilmente editables sin tocar el código fuente.

## Construcción del Modelo
La arquitectura del núcleo lógico (todo lo que reside en la carpeta `modelo`) está diseñada siguiendo principios de modularidad y bajo acoplamiento. He dividido el sistema en varios submódulos especializados para facilitar el mantenimiento y delegar responsabilidades específicas a distintos agentes:

### 1. Clases y Estructuras Base (`modelo/clases/` y `modelo/game/`)
Aquí residen las entidades que mantienen la persistencia, memoria y las reglas de negocio del juego.
```mermaid
classDiagram
    class Campania {
        +String estado_ui
        +ContextoJuego contexto
        +EstadoJuego estado
        +MensajeJuego mensaje
        +reiniciar()
        +recibir_accion_jugador(accion)
        +arbitrar_accion_jugador()
        +resolver_tirada()
        +no_requiere_tirada()
        +narracion()
        +orquestador()
        +verificar_finales()
        +habla_personaje()
        +generar_imagen_resumen()
        +obtener_mensaje_vista()
        +limpiar_mensaje()
        +narracion_final()
    }

    class EstadoJuego {
        +String ubicacion
        +List eventos
        +List decisiones
        +List personajes_presentes
        +Dict estados_personajes
        +List objetos_heroe
        +String final
        +set_ubicacion(ubicacion)
        +get_ubicacion()
        +agregar_evento(evento)
        +agregar_decision(decision)
        +agregar_personaje(personaje)
        +quitar_personaje(personaje)
        +set_final(final)
        +get_final()
        +set_estado_personaje(personaje, estado)
        +get_estado_personaje(personaje)
        +agregar_objeto_heroe(objeto)
        +quitar_objeto_heroe(objeto)
        +obtener_imagenes_escena()
        +obtener_rutas_imagenes_personajes()
        +to_dict()
    }

    class ContextoJuego {
        +String prompt_jugador
        +boolean accion_valida
        +boolean requiere_tirada
        +int dificultad
        +EstadoJuego estado
        +String resultado_d20
        +set_prompt_jugador(prompt)
        +get_prompt_jugador()
        +set_accion_valida(accion_valida)
        +get_accion_valida()
        +set_requiere_tirada(requiere_tirada)
        +get_requiere_tirada()
        +set_dificultad(dificultad)
        +get_dificultad()
        +set_estado(estado)
        +get_estado()
        +set_resultado_d20(resultado)
        +get_resultado_d20()
        +set_exito()
        +mostrar()
        +to_dict()
    }

    class MensajeJuego {
        +String narracion
        +String imagen_resumen
        +String narracion_npc
        +String imagen_npc
        +hay_dialogo_npc()
        +obtener_seccion_obligatoria()
        +obtener_mensaje_completo()
        +set_narracion(narracion)
        +get_narracion()
        +set_imagen_resumen(imagen_resumen)
        +get_imagen_resumen()
        +set_narracion_npc(narracion_npc)
        +get_narracion_npc()
        +set_imagen_npc(imagen_npc)
        +get_imagen_npc()
        +set_dialogo_npc(narracion_npc, imagen_npc)
        +limpiar_dialogo_npc()
    }

    Campania *-- ContextoJuego
    Campania *-- EstadoJuego
    Campania *-- MensajeJuego
```
- **Campania.py**: Es el cerebro organizador; mantiene el contexto de la partida activa, orquesta las llamadas a la IA y administra el flujo general del juego.
- **Estadojuego.py** y **ContextoJuego.py**: Almacenan y serializan (a JSON) los datos del mundo, los inventarios, estadísticas y salud de los personajes.
- **MensajeJuego.py**: Define de forma estándar la estructura de los diálogos y notificaciones que se enviarán a la Vista.
- **Submódulo `game/`**: Incluye archivos de soporte (`characters.py`, `items.py`, `campaign.py`) para definir y estructurar los atributos crudos de los actores, campañas y objetos.

### 2. Motores de Inteligencia Artificial (`modelo/ai/`)
El flujo de juego funciona como un ciclo continuo (Game Loop) donde la acción del jugador pasa por una "cadena de montaje" de **Agentes de IA Especializados**. Estos agentes se comunican entre sí y modifican el **Estado de la partida** central en cada turno:

```mermaid
flowchart LR
    Jugador([Jugador])
    Arbitro[Árbitro de acción]
    Tirada[Tirada de d20]
    Orq[Orquestador de estado]
    Dialogador[Dialogador]
    Narrador[Narrador]
    Verif[Verificador de finales]
    GenVis[Generador de imágenes]
    Estado[(Estado de la partida)]

    Jugador -- acción --> Arbitro
    Arbitro -- requiere tirada --> Tirada
    Tirada -- resultado --> Orq
    Arbitro -- sin tirada --> Orq
    
    Orq -- actualiza --> Estado
    Orq --> Dialogador
    Dialogador --> Narrador
    Narrador --> Verif
    Verif --> GenVis
    GenVis -- respuesta --> Jugador

    Arbitro -. lee .-> Estado
    Narrador -. lee .-> Estado
    Verif -. lee .-> Estado
```

**Explicación detallada de cada Agente y Componente:**

- **Árbitro de Acción (`arbitro_accion.py`)**: Es el primer filtro cognitivo. Analiza lo que el jugador intenta hacer y decide de forma objetiva si es una acción trivial (ej: "Miro el cielo") o si existe un riesgo que requiere aplicar las reglas del juego (ej: "Salto el abismo"). Si hay riesgo, exige lanzar una *Tirada de d20*.
- **Orquestador de Estado (`Orquestador_estado.py`)**: Es el administrador de los datos duros. Recibe el desenlace matemático (éxito, fracaso, daño, etc.) y decide *qué cambia físicamente* en el mundo: actualiza la salud, mueve los objetos del inventario y define transiciones de sala. Luego, guarda estos datos en el JSON del estado de la partida.
- **Dialogador (`dialogador.py`)**: Cuando la escena involucra personajes (NPCs), este agente "actúa" asumiendo su personalidad. Reacciona a las acciones del jugador generando diálogos que encajan con las emociones y secretos del NPC.
- **Narrador (`narrador.py`)**: Cumple el rol del clásico Dungeon Master literario. Junta todo lo que acaba de suceder (consecuencias físicas, resultados de dados, diálogos) y redacta la respuesta inmersiva definitiva que describe la escena para el jugador.
- **Verificador de Finales (`Verificador_finales.py`)**: Trabaja de manera invisible en segundo plano. Tras cada turno, escanea silenciosamente el estado del mundo para comprobar si el jugador ha ganado, ha muerto o ha disparado algún final secreto de la campaña.
- **Generadores Visuales (`generador_imagen_escena.py`, `imagen_NPC.py`)**: Son la parte "artística". Al terminar de construir la narrativa, extraen un resumen visual y elaboran *prompts* detallados que se envían a generadores de imágenes (como Stable Diffusion) para ilustrar la pantalla final.
- **Capa de Clientes API (`GeminiClient.py`, `LocalAIClient.py`)**: Es la vía de comunicación. Todos los agentes mencionados anteriormente son posibles gracias a esta capa que envía y recibe información de los "cerebros" reales: ya sea el modelo de Google en la nube (Gemini) o los modelos locales en tu PC vía Ollama (administrados automáticamente por `ollama_manager.py`).

### 3. Herramientas ("Tool Calling") (`modelo/tools/`)
Para evitar que los modelos de lenguaje "alucinen" resoluciones mecánicas, he implementado funciones de código estricto que las IAs pueden invocar:
- **`dice.py`**: Ejecuta lógicamente las tiradas de dados (d20) y verifica si una acción es un éxito o un fracaso matemático basado en el estado.
- **`gen_state.py` y `gen_messege.py`**: Rutinas controladas para que la IA actualice atributos (vida, inventario) o emita alertas sin corromper el motor de juego.

### 4. Configuración (`modelo/configuracion.py`)
Módulo encargado de aislar la persistencia de los ajustes del usuario, leyendo y escribiendo en el `config.json` parámetros clave como el motor de IA seleccionado.

## Construcción de la Vista Gráfica
La interfaz gráfica de usuario (GUI) ha sido diseñada pensando en la usabilidad y la experiencia del usuario. Busca proporcionar un entorno limpio y directo donde el usuario pueda escribir sus prompts, configurar los parámetros del modelo en tiempo real y visualizar las respuestas de forma estructurada. La vista se comunica de forma asíncrona con los clientes de IA para mantener la aplicación receptiva incluso durante tiempos de inferencia prolongados.

## Demostración de Partida
A continuación, se muestra el flujo típico de una sesión de juego interactuando con el Director de Juego (DM):

### 1. Escena Inicial y Generación Visual
El DM nos sitúa en el contexto mediante una descripción narrativa detallada, acompañada de una imagen generada por IA que ilustra nuestra ubicación actual.
![Juego con imagen generada](modelo/game/assets/Readmee/Juego_con_imagen_generada.jpg)

### 2. Resolución de Acciones (Tirada de d20)
Cuando intentamos una acción arriesgada (como atacar o escapar), el "Árbitro" interviene automáticamente y exige una tirada de dados virtual para determinar nuestro éxito.
![Tirada d20](modelo/game/assets/Readmee/tirada_d20.jpg)

### 3. Consecuencia Matemática (Resultado)
El motor calcula el resultado evaluando la dificultad y la tirada. A partir de este número, la IA describe narrativamente cómo nos fue (un fallo desastroso o un éxito épico).
![Resultado d20](modelo/game/assets/Readmee/resultado_d20.jpg)

### 4. Interacción con NPCs
El sistema puede asumir la identidad de cualquier personaje, permitiendo diálogos inmersivos y mostrando el retrato del NPC con el que estamos conversando.
![Diálogo NPC](modelo/game/assets/Readmee/Dialogo_npc.jpg)

### 5. Evaluación de Objetivos
El Verificador de finales analiza en segundo plano nuestras acciones. Si detecta que hemos completado la misión (o muerto en el intento), nos alerta sobre el desenlace inminente.
![Confirmación de Final](modelo/game/assets/Readmee/Final_confirm.jpg)

### 6. Pantalla Final
La aventura concluye y se cierra la sesión tras resolver el desenlace de la historia.
![Pantalla Final](modelo/game/assets/Readmee/final.jpg)

## Trabajo Futuro
El proyecto se encuentra en constante evolución. Algunas de mis metas para futuras versiones incluyen:
- **Soporte para más proveedores de IA**: Integración con OpenAI, Anthropic y otras alternativas locales como Ollama.
- **Gestión avanzada de contexto y memoria**: Mejorar la capacidad del modelo para recordar conversaciones largas y mantener el contexto.
- **Mejoras en la Interfaz Gráfica**: Añadir soporte para temas (modo oscuro/claro), atajos de teclado y exportación de conversaciones a PDF/Markdown.
- **Procesamiento Multimodal**: Ampliar las capacidades para que el sistema pueda analizar y responder a imágenes y documentos, no solo a texto.
- **Optimización de Código**: Refactorizar y limpiar la base de código para reducir la latencia, especialmente en el manejo de peticiones locales y renderizado gráfico.
- **Mejoras en la Arquitectura**: Consolidar el patrón de diseño (como MVC) para lograr un mayor desacoplamiento entre la lógica del juego (modelo) y Pygame (vista), lo que facilitaría escalar el proyecto o incluso llevarlo a la web en el futuro.
