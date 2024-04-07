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
   <div>Imagen dilatada</div>
</div> 


## Despliegue <a name="id3"></a>
### Requisitos
- Python 3.10
- Control de versiones git

### Preparación del entorno
Clonar el repositorio:

```
git clone https://github.com/ariano-m/AIVA_2024_MADERAS.git
cd AIVA_2024_MADERAS
```

Para instalar las dependencias necesarias únicamente para este proyecto, se puede crear un entorno virtual con el siguiente comando:
```
python -m venv venv
```
Para activar el entorno virtual se ha de ejecutar el archivo _activate_.

En Unix o MacOS, ejecuta:
```
source venv/bin/activate
```
En Windows, ejecuta:
```
venv\Scripts\activate.bat
```
Para instalar las diferentes versiones de las [librerías](https://github.com/ariano-m/AIVA_2024_MADERAS/blob/main/requirements.txt) utilizadas:

```
pip install -r requirements.txt
```
Para asegurarse de que el directorio actual está en el path de python.

En Unix o MacOS, ejecuta:
```
export PYTHONPATH="${PYTHONPATH}:/my/other/path"
export PYTHONPATH=$PYTHONPATH:'pwd'
```
En Windows, ejecuta:
```
set PYTHONPATH=%PYTHONPATH%;C:\My_python_lib
```

### Lanzar programa
Primero se ha de estar en la carpeta del proyecto donde se situa main.py. En este caso, se encuentra en _AIVA_2024_MADERAS/bin/server/system/main.py_.
```
cd bin/server/system/
```
El comando para ejecutar el sistema y que este nos devuelva una imagen con las piezas colocadas sería el siguiente:
```
python <ruta donde se encuentra el main.py> --img_path <ruta de la imagen>
```
Un ejemplo, si nos encontramos en la carpeta _system_:
```
python main.py --img_path ../../../dataset/MuestrasMaderas/10.png
```

### Lanzar test
Al igual que la anterior vez, se ha de ir a la carpeta donde se encuentran los test. En este caso es _AIVA_2024_MADERAS/bin/server/tests_.
```
cd bin/server/tests
```
El comando para ejecutar el test sería el siguiente:
```
python <ruta donde se encuentra el test.py> <ruta del modelo (opcional)> <ruta de la imagen (opcional)>
```
A continuación, se muestra un ejemplo de ejecución para casa test.

**test_system**:
```
python test_system.py ../../../dataset/MuestrasMaderas/10.png
```
**test_model**:
```
python test_model.py ../models/Yolo_Training2/weights/best.pt ../../../dataset/MuestrasMaderas/62.png
````
**test_trainer**:
```
python test_trainer.py ../models/Yolo_Training2/weights/best.pt
```
