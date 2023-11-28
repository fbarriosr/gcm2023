# Descargamos de Dockerhub la version 3.8 de python
FROM python:3.8

# Para poder leer mensajes de la consola de python en la ejecucion
ENV PYTHONUNBUFERED 1

# Creamos el directorio para almacenar el contenido del proyecto
RUN mkdir /code

# Definimos /code como el directorio de trabajo
WORKDIR /code

# Copiamos el archivo de requerimientos al directoio de trabajo
COPY requirements.txt /code/

# Instalamos los requerimientos descritos en requirements.txt
# -m para qque se ejecute con la misma version pip del proyecto
RUN python -m pip install -r requirements.txt

# Cipiamos el contenido del proyecto al directorio de trabajo /code
COPY . /code/