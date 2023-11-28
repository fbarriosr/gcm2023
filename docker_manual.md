## COMANDOS DOCKER PARA DESARROLLO

### PARA COMPILAR LA BASE DE DATOS

```
$ docker-compose run web python manage.py makemigrations
$ docker-compose run web python manage.py migrate
```

### CREAR SUPER USER 

```
$ docker-compose run web python manage.py createsuperuser
```

### ENTRAR AL ENTORNO DIRECTORIO

```
$ docker exec -it web bash
```

### ELIMINA CONTENDORES PARADOS

```
$ docker prune
```

### ELIMINAR CONTENEDOR

```
$ docker rm contenedor
```

### VER IMAGES

```
$ docker images 
o 
$ docker image list
```

### DESCARGA IMG
```
$ docker pull nombre
```

### REMOVE IMAGE
```
$ docker image rm 
```

### BORRAR IMAGENES
```
$ docker system prune -a
```

### VER CONENEDORES
```
$ docker ps
```

### DOCKER GUARDAR TODAS LAS IMAGES
```
$ docker save $(docker images --format '{{.Repository}}:{{.Tag}}') -o allinone.tar

$ docker save -o /home/matrix/matrix-data.tar matrix-data
```
### CARGAR IMAGEN DESDE ARCHIVO
```
$ docker load -i allinone.tar
```

### ELIMINA CONTENDORES PARADOS
```
$ docker container prune
```


### CONSTRUIR IMAGEN
```
$ docker build -t nombre_contenerdor .
```

### RUN
Ejecuta por 1 vez hay que colocar nombre al contenedor  sino docker le pone uno de cinetifico

```
$ docker run 

$ docker run -it --name contenedor imagen
```
