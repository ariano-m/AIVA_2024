# AIVA_2024_MADERAS

Desarrolladores de VisionaryAI:
 - Adrián Riaño Martínez
 - Irene García Rubio

## Índice
1. [Introducción](#id1)
2. [Dataset](#id2)
3. [Despliegue](#id3)


## Introducción <a name="id1"></a>
La empresa **El Bosque de Juguetes** se dedica a realizar juguetes de maderas de forma manual. Para ello, obtiene una tabla de madera, toma una foto y con un software dibuja las piezas de un tamaño predefinido.
El trabajador se enfrenta a que el proceso manual requiere mucho tiempo y considera que la automatización le reportará más beneficios por el aumento de producción. Por tanto, en este proyecto, se propone el diseño de un sistema de visión artificial que sea capaz de reconocer los defectos en las tablas de madera y decida la posición de las piezas a obtener. 
Uno de los requerimientos del cliente se trata de que el sistema trabaje sobre un aplicación móvil, ya que es la herramienta que utiliza. Con este motivo, se plantea una arquitectura cliente-servidor. El cliente (móvil) tomará una foto, y la aplicación se conectará al servidor para enviarle la imagen. Después, el servidor realizará los cálculos y devolverá el resultado al cliente.

El sistema desarrollado para resolver esta necesidad se conoce como **ToyWoodVision** y se encargará de su implementación la compañía **VisionaryAI**.

## Dataset <a name="id2"></a>
La base de datos proporcionada por el cliente es una recopilación de 79 imágenes de tablones de madera sobre fondo negro. Aunque la iluminación parece constante, hay un cierto número de imágenes que presentan una tonalidad de madera más oscura.


Imagen 36             |  Imagen 37
:-------------------------:|:-------------------------:
![](https://github.com/ariano-m/AIVA_2024_MADERAS/blob/main/dataset/MuestrasMaderas/25.png) | ![](https://github.com/ariano-m/AIVA_2024_MADERAS/blob/main/dataset/MuestrasMaderas/37.png)

Parte de la solución a implementar consiste en detectar los nodos o grietas que pueda presentar la madera.
- Los nodos se definen como el área de tejido leñoso resultante de la huella dejada por el desarrollo de una rama.
- Las grietas son la separación de las fibras (corte o hendidura) en dirección longitudinal.

A continuación, se muestra un ejemplo del objetivo:
<div align="center">
    <img src="https://github.com/ariano-m/AIVA_2024_MADERAS/assets/35432675/1adf935e-fe37-48d6-a50c-75f8982ac808" width="450">
   <div>Detección de imperfecciones</div>
</div> 


## Despliegue <a name="id3"></a>
### Requisitos
- Python 3.10
- Control de versiones git
- Docker \& Docker-compose
- Teléfono Android o IOS

### Preparación del entorno
Clonar el repositorio:

```
git clone https://github.com/ariano-m/AIVA_2024_MADERAS.git
cd AIVA_2024_MADERAS
```
### Despliegue del Docker
A continuación, se realiza una llamada a docker-compose para crear los diferentes servicios que contiene el proyecto:
```
docker-compose up -d
```
También se puede desplegar usando la imagen alojada en DockerHub:
```
docker pull wariano/maderas_visionaryai:init
docker image ls  # show our image downloaded
docker run -d --name visionaryai -p 5005:5005 -p 3306:3306 wariano/maderas_visionaryai
```


### Aplicación móvil
La aplicación se entrega al cliente como un archivo APK que los empleados pueden instalar en sus dispositivos móviles. Por tanto, con copiar la aplicación al dispositivo móvil e iniciando la APK, se instalará.
```
/bin/client/app/flutter_application_1/build/app/outputs/flutter-apk/
```
