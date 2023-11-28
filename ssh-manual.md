## COMANDOS PARA CREAR LLAVE SSH

### CREAR LLAVE SSH 
```
$ ssh-keygen -t rsa -b 4096 -C "poner aquí correo electrónico"  // correo que aparece en tu cuente de github

ssh-keygen: Generador de ssh keys
-t rsa: Transforma la key con el algoritmo de rsa (podria ser sha, etc. Github propone rsa)
-b 4096: Github propone este numero de bits para nuestras keys
-C : "email aqui"
```
#### Por ejemplo 
```

$ ssh-keygen -t rsa -b 4096 -C “francisco.barriosr@gmail.com”

```

### VER LLAVE CREADA
```
$ cd  ~/.ssh
$ cat id_rsa.pub
```

### Copiamos la llave y la pegamos en Settings > SSH, dentro de GitHub.
