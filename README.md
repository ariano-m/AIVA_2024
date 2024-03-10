# AIVA_2024_MADERAS

Desarrolladores de VisionaryAI:
 - Adrián Riaño Martínez
 - Irene García Rubio

## Índice
1. [Introducción](#id1)


## Introducción <a name="id1"></a>
La empresa **El Bosque de Juguetes** se dedica a realizar juguetes de maderas de forma manual. Para ello, obtiene una tabla de madera, toma una foto y con un software dibuja las piezas de un tamaño predefinido.
El trabajador se enfrenta a que el proceso manual requiere mucho tiempo y considera que la automatización le reportará más beneficios por el aumento de producción. Por tanto, en este proyecto, se propone el diseño de un sistema de visión artificial que sea capaz de reconocer los defectos en las tablas de madera y decida la posición de las piezas a obtener. 
Uno de los requerimientos del cliente se trata de que el sistema trabaje sobre un aplicación móvil, ya que es la herramienta que utiliza. Con este motivo, se plantea una arquitectura cliente-servidor. El cliente (móvil) tomará una foto, y la aplicación se conectará al servidor para enviarle la imagen. Después, el servidor realizará los cálculos y devolverá el resultado al cliente.

El sistema desarrollado para resolver esta necesidad se conoce como **ToyWoodVision** y se encargará de su implementación la compañía **VisionaryAI**.
