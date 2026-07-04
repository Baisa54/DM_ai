#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# Vista_Grafica
#
# Este programa es la vista grafica de la aplicacion DM AI
# La idea general es hacer una taberna de fondo con una imagen,
# Luego, abajo una barra de chat en conjunto con un boton enviar
# Para que el usaurio escriba sus acciones.
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ Imagen de fondo de una taberna.
# @ Barra inferior de madera
# @ [En barra inferior] Boton enviar
# @ [En barra inferior] chat para escribir la accion del usuario
# @ Pergamino donde se narra historia
# @ Pergamino donde se muestra imagen resumen
# @ Pergamino (Opcional) donde se muestra texto generado por un personaje
# @ Pergamino (Opcional) donde se muestra imagen NPC
# @ Barra superior de madera
# @ [En barra superior] Boton para estado
# @ [En barra superior] Boton reiniciar aventura
# @ [En barra superior] Imagen DM_ai con gorro
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS DEL USUARIO
#
# @ Accion escrita & Boton enviar (Enviar accion)
#   --> Se valida si hay algo escrito
#   --> Si no hay nada escrito, se muestra mensaje de error
#   --> Si hay algo escrito, se muestra mensaje de que se esta procesando
#
# @ Accion de Boton de estado
#   --> Se muestra una ventana emergente
#   --> La ventana posee boton de salida
#   --> La ventana muestra el estado de la partida
#
# @ Accion de Boton reiniciar 
#   --> Se muestra una ventana emergente
#   --> La ventana muestra que una vez realizada la accion no hay vuelta atras
#   --> Posee un boton de 'Reiniciar' que reinicia la partida
#   --> Posee un boton de 'Cancelar' que cierra la ventana 
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

