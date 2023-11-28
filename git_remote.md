## COMANDOS REMOTO GIT PARA DESARROLLO

### PARA INICIAR UN PROYECTO EN GIT USAR:

```
$ git init
```

### AGREGAR REPOSITORIO REMOTO A GIT 
```
$ git remote add origin sshrutaRepositorio
```

### SUBIR A REPOSITORIO REMOTO  
```
$ git push origin master   
```

### VEO LOS REPOSITORIOS REMOTOS
```
$ git remote -v  
```

### REMOVER LOS REPOSITORIOS REMOTOS
```
$ git remote  rm origin  
```

### GIT FETCH+ GIT MERGE
```
$ git remote add origin [ssh]
$ git fetch origin 
$ git merge origin/master
```

### PARA DESARROLLADORES
```
$ git fetch origin
$ git merge origin/master
$ git push origin master
```

### VER RAMAS DESCARGADAS 
```
$ git branch -a
```

### CAMBIAR Y CREAR RAMA
```
$ git checkout -b nombre_rama
```




