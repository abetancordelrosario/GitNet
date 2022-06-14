<p align="center">
  <img src="https://github.com/abetancordelrosario/GitNet/blob/main/docs/images/logo-recortado.png" width="150" height="100" />
</p>

## Aplicación para el análisis de comunidades en GitHub basándose en grafos de interés.
Este Trabajo Fin de Título desarrollado en la Universidad de Las Palmas de Gran Canaria (ULPGC) tiene como objetivo analizar las comunidades que se forman alrededor de los distintos proyectos en GitHub creando un grafo a partir de los <i>stargazers</i> y otros repositorios que le interesan a estos, para luego extraer información relevante mediante el uso de algoritmos como <i>PageRank</i> y técnicas de <i>machine learning</i> empleando <i>XGBoost</i>.

### Requisitos
* Docker 20.10.12
* Python 3.10.1

Se recomienda utilizar Visual Studio Code como IDE ya que dispone de múltiples extensiones que facilitan trabajar con Docker o lenguajes de programación como Python.

### Instalación
Para descargar la aplicación primero de ejecuta.
```
git clone https://github.com/abetancordelrosario/GitNet.git
```

Luego, para construir la imágen de docker y ejecutarla.
```
docker build --pull --rm -f "Dockerfile" -t gitnet:latest "."

docker run -it gitnet:latest /bin/bash
```

Finalmente para ejecutar la aplicación.
```
/bin/python /app/src/main.py -r <nombre completo repositorio> -t <token OAuth>
```
Sin embargo, se recomienda utilizar la herramienta <i>remote containers</i> de VScode ya que automatiza el proceso de construir y ejecutar la imágen. En este caso el comando para ejecutar la aplicación sería.
```
/bin/python /workspaces/GitNet/src/main.py -r <nombre completo repositorio> -t <token OAuth>
```

### Recursos

Las principales librerías empleadas en el proyecto fueron, <b>asyncio</b> y <b>aiohttp</b> para la extracción de los datos de la API, <b>graph-tool</b> para la creación del grafo y para aplicar los algoritmos, <b>matplotlib</b> para la generación de gráficas, <b>Python Prompt Toolkit</b> en el desarrollo del CLI y <b>XGBoost<b>, </b>pandas</b>, <b>scikit learn</b> y <b>numpy</b> para la creación del modelo ML.

### Funcionamiento
La aplicación dispone de una interfaz por línea de comandos donde se introducen dos parámetros, el nombre completo del repositorio (creador/repositorio) y el token de autenticación de la cuenta del usuario (OAuth). En el supuesto de que los argumentos sean válidos, se extrae concurrentemente, empleando técnicas de programación asíncrona la información de la API de GitHub acerca del repositorio. Una vez extraída la información, se generá un grafo de interés y la aplicación pasaría a funcionar como un  <i>shell</i>. Entre las opciones disponibles se encuentran, obtener los repositorios más relevantes, los usuarios más importantes, los lenguajes de pogramación, tópicos y licencias que más les interesan o aplicar machine learning para extraer los repositorios más relevantes consuminedo menos recursos. También se generarán una serie de gráficas representando los resultados, además de poder visualizar el grafo. 

