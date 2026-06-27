# Documento Técnico: Flujo CI/CD para Django

Este documento detalla la arquitectura y el funcionamiento del pipeline de Integración Continua (CI) y simulación de Despliegue Continuo (CD) configurado para este proyecto Django.

---

## 1. Diagrama del flujo CI/CD

El siguiente diagrama ilustra visualmente el ciclo de vida del código desde que el desarrollador hace un `push` hasta que la aplicación es desplegada en el entorno simulado.

```mermaid
graph TD
    A[Desarrollador hace Push a main] --> B(GitHub Actions se activa)
    
    subgraph Fase de Integración Continua (CI)
    B --> C{Levantar PostgreSQL}
    C --> D[Instalar Dependencias]
    D --> E[Ejecutar Tests Django]
    end
    
    subgraph Fase de Construcción (Build)
    E --> F[Construir Imagen Docker]
    F --> G[Guardar Artefacto .tar]
    end
    
    subgraph Fase de Despliegue Simulado (CD)
    G --> H[Clonar / Descargar en Servidor Externo]
    H --> I[docker compose up -d]
    I --> J[Ejecutar Migraciones]
    J --> K((App en Producción))
    end
```

---

## 2. Explicación del archivo `.github/workflows/ci.yml`

El archivo de GitHub Actions es el motor de nuestro flujo automatizado. A continuación, se explica paso a paso lo que hace:

1. **Eventos (Triggers):** 
   ```yaml
   on:
     push:
       branches: [ "main", "master" ]
   ```
   *El pipeline se dispara automáticamente cada vez que se sube código a las ramas principales, garantizando que el código nuevo siempre sea evaluado.*

2. **Servicios (Base de Datos para Tests):**
   ```yaml
   services:
     postgres:
       image: postgres:15
   ```
   *Levanta un contenedor de PostgreSQL temporal dentro de GitHub Actions exclusivamente para que los tests de Django puedan ejecutarse contra una base de datos real.*

3. **Preparación del Entorno:**
   ```yaml
   - uses: actions/checkout@v4
   - uses: actions/setup-python@v5
   ```
   *Descarga el código fuente al servidor de GitHub y configura Python en la versión 3.12, dejándolo listo para trabajar.*

4. **Instalación y Pruebas:**
   ```yaml
   - name: Run Django Tests
     run: python manage.py test
   ```
   *Instala las librerías del `requirements.txt` y corre las pruebas unitarias. Si una prueba falla, el pipeline se detiene aquí y se bloquea el despliegue.*

5. **Construcción y Artefactos (Docker):**
   ```yaml
   - name: Build Docker Image
     run: docker build -t gestion-web:latest .
   ```
   *Si los tests pasan, procede a compilar el `Dockerfile`, empaquetando la aplicación en una imagen de contenedor. Luego, guarda esta imagen como un archivo `.tar` en los Artefactos de GitHub para que el servidor de producción pueda descargarla.*

---

## 3. Recomendaciones Finales

Para escalar este proyecto a un entorno de producción real, se recomiendan las siguientes mejoras:

- **Uso de un Container Registry:** En lugar de guardar la imagen como un artefacto `.tar`, se debe integrar un paso para hacer `docker push` hacia un registro como **DockerHub**, **AWS ECR** o **GitHub Container Registry**.
- **Manejo de Secretos:** Nunca exponer claves como el `SECRET_KEY` de Django o la contraseña de base de datos en código duro. Utilizar **GitHub Secrets** y pasarlos como variables de entorno al contenedor.
- **Protección de Ramas:** Configurar GitHub para que no permita hacer `push` directamente a `main`, sino que requiera un Pull Request que obligatoriamente deba pasar este pipeline de CI antes de poder fusionarse (Merge).
- **Despliegue 100% Automatizado:** Usar herramientas como SSH, AWS CodeDeploy o un orquestador (Kubernetes/Docker Swarm) en un paso de despliegue dentro del mismo `.yml` para que el servidor se actualice solo sin necesidad de simulación manual.
