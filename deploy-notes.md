# Notas de Despliegue Simulado (Deploy Notes)

Este documento detalla los pasos para simular un despliegue continuo de la aplicación en un entorno de producción (o una carpeta externa del sistema local).

## 1. Descargar el Proyecto (Simulación de Servidor)

Para simular el entorno del servidor, debes clonar el proyecto (que ya fue probado y empaquetado por GitHub Actions) en una nueva carpeta en tu sistema operativo:

```powershell
# Moverte a una ubicación externa, como Documentos o el Escritorio
cd C:\Users\Luis\Documents

# Descargar el proyecto desde GitHub (asegúrate de que los cambios estén subidos a tu repositorio)
git clone https://github.com/Luisst32/gestion_.git despliegue_produccion

# Entrar a la nueva carpeta
cd despliegue_produccion
```

> **Nota:** En un entorno real, el servidor también podría descargar el artefacto `.tar` directamente desde GitHub Actions usando la API de GitHub, pero usar `git pull` o `git clone` y reconstruir localmente también es un estándar de simulación válido.

## 2. Ejecutar con Docker Compose

Dado que la aplicación ya está contenerizada, no necesitas configurar Python ni PostgreSQL manualmente en este entorno de despliegue. Docker se encargará de todo.

Ejecuta el siguiente comando para levantar el entorno en "modo detached" (segundo plano), que es como corren los servidores en producción:

```powershell
docker-compose up -d --build
```

Esto hará lo siguiente:
1. Construirá la imagen del contenedor `web` (Django).
2. Descargará y levantará el contenedor `db` (PostgreSQL).
3. Conectará ambos servicios en la misma red.

### Aplicar Migraciones en el Despliegue
Como es un nuevo servidor, la base de datos estará vacía. Aplica las migraciones:
```powershell
docker-compose exec web python manage.py migrate
```

## 3. Validar desde el Navegador

Una vez que los contenedores reporten estar `Running` (puedes verificarlo con `docker-compose ps`), abre tu navegador web y dirígete a:

 **[http://localhost:8000](http://localhost:8000)**

Deberías poder visualizar la interfaz moderna del CRUD de **Productos**, verificar que los listados cargan correctamente y que se pueden agregar nuevos registros, confirmando que la base de datos PostgreSQL está operando dentro del contenedor.

### Pasos para detener el servidor
Si deseas apagar el entorno de producción simulado:
```powershell
docker-compose down
```
