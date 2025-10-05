# Análisis de Videojuegos - Proyecto Dockerizado

## Descripción
Proyecto de análisis de datos de videojuegos.

---

## Estructura del Proyecto

```
proyecto-videojuegos/
│
├── Dockerfile                    # Definición de la imagen Docker
├── docker-compose.yml            # Orquestación de servicios
├── requirements.txt              # Dependencias Python
├── .dockerignore                 # Archivos excluidos del build
├── analisis_videojuegos.py       # Script principal de análisis
│
├── data/                         # Dataset
│   └── vgsales.csv              
│
├── output/                       # Resultados generados
    └── analisis_videojuegos.png
```

---

## Inicio Rápido

### **Iniciar todos los servicios**
```bash
docker-compose up -d
```

### **Ver logs**
```bash
docker-compose logs -f
```

### **Detener servicios**
```bash
docker-compose down
```

---

## Outputs Generados

Después de ejecutar el análisis, encontrarás en `output/`:

- **analisis_videojuegos.png** - Gráficas del análisis
- **Logs en consola** - Estadísticas y validación de hipótesis

---

## Repositorio en el que se encuentra. 

Este es el repositori donde se encuentra el codigo fuente del proyecto 

GIT: https://github.com/rivalTj7/Mini-Proyecto-01.git
