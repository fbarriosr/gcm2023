## COMANDOS GIT LOCAL PARA DESARROLLO

### DESCARGAR UN PROYECTO DESDE GITHUB SIN COLABORAR (GIT CLONE)
```
$ git clone [repositorio]
```

### PARA INICIAR UN PROYECTO EN GIT USAR:

```
$ git init
```

### PARA PASAR LOS ARCHIVOS A STAGE:
```
$ git add nombre archivo
```

### PARA HACER UN COMMIT:
```
$ git commit -m "nombre del commit"
```

### SABER EL ESTADO:
```
$ git status
```

### SABER LA RAMA:
```
$ git branch (para ver en que rama estás ubicado)
```
### BORRAR 
```
$ git reset --hard commiID
```
### GIT ADD+ COMMIT
```
$ git commit -m "cambio 3"
```

### GIT AMMED (CAMBIA EL ULTIMO COMMIT A UNO ACTUALIZADO)
```
$ git commit -m "cambio 3 final" --amend
```

### CAMBIAR DE EL PUNTERO HEAD
```
$ git checkout commintID
```

### REGRESAR AL ULTIMO COMMIT DE MASTER
```
$ git checkout master
```


### GIT LOGs:
```
$ git log -m "mensaje"  --amend = Rectifica y sustituye el ultimo commit
$ git log --oneline = muestra el commit resumido en una linea
$ git log --decorate = muestra el commit con el head indicado donde esta posicionado 
$ git log --stat = explica con detalle en numero de lineas que se conbinaron.
$ git log -p = es un análisis más profundo del anterior (git log --stat).
$ git shortlog =   agrupa por autor y muestra los titulos del commit.
$ git log --graph --oneline --decorate = muestra grafica del de historial del repositorio.

$ git logs filtros de comandos
$ git log -3 =  Por cantidad muestra los comiits
$ git log --before="today"  = se muestra todo lo de antes de hoy
$ git log --after="today"  = se muestra todo lo de mañana 
$ git log --author ="AUTOR" = muestra los commits dle autor
$ git log --grep="MENSAJE" = muestra el todo los commit que concuerden con el mensaje (el mensaje debe de estar en el titulo  ) sencible a MAyusculas o minusculas usar el i al final 
$ git log -- archivo.* = comits por archivo (el * extencion del archivo php.html.py etc etc )
```
