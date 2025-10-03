# 🎮 Análisis de Videojuegos - Proyecto Dockerizado

## 📋 Descripción
Proyecto de análisis de datos de videojuegos completamente dockerizado para garantizar portabilidad y no consumir recursos locales.

---

## 🗂️ Estructura del Proyecto

```
proyecto-videojuegos/
│
├── Dockerfile                    # Definición de la imagen Docker
├── docker-compose.yml            # Orquestación de servicios
├── requirements.txt              # Dependencias Python
├── Makefile                      # Comandos simplificados
├── .dockerignore                 # Archivos excluidos del build
├── analisis_videojuegos.py       # Script principal de análisis
│
├── data/                         # 📂 Dataset (crear manualmente)
│   └── vgsales.csv              # ⚠️ Descargar de Kaggle
│
├── output/                       # 📂 Resultados generados
│   └── analisis_videojuegos.png # Gráficas generadas
│
└── notebooks/                    # 📂 Jupyter notebooks (opcional)
    └── exploracion.ipynb
```

---

## 🚀 Inicio Rápido

### **Paso 1: Preparar el entorno**

```bash
# Crear estructura de carpetas
make setup
```

### **Paso 2: Descargar dataset**

1. Ve a [Kaggle - Video Game Sales](https://www.kaggle.com/datasets/gregorut/videogamesales)
2. Descarga `vgsales.csv`
3. Colócalo en la carpeta `data/`

```bash
proyecto-videojuegos/
└── data/
    └── vgsales.csv  ✅
```

### **Paso 3: Construir imagen Docker**

```bash
make build
```

### **Paso 4: Ejecutar análisis**

```bash
make run
```

**¡Listo!** Los resultados estarán en `output/analisis_videojuegos.png`

---

## 📝 Comandos Disponibles

### **Comandos Básicos**

| Comando | Descripción |
|---------|-------------|
| `make help` | Muestra todos los comandos disponibles |
| `make setup` | Crea estructura de carpetas |
| `make build` | Construye la imagen Docker |
| `make run` | Ejecuta el análisis completo |
| `make stop` | Detiene todos los contenedores |
| `make clean` | Limpia contenedores e imágenes |

### **Comandos Avanzados**

| Comando | Descripción |
|---------|-------------|
| `make jupyter` | Inicia Jupyter Notebook en http://localhost:8888 |
| `make logs` | Ver logs del análisis |
| `make shell` | Entrar al contenedor (bash interactivo) |
| `make up` | Iniciar con docker-compose |
| `make down` | Detener docker-compose |

---

## 🐳 Uso con Docker (sin Makefile)

Si prefieres usar comandos Docker directamente:

### **Construir imagen**
```bash
docker build -t videogame-analysis .
```

### **Ejecutar análisis**
```bash
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/output:/app/output \
  videogame-analysis
```

### **Jupyter Notebook**
```bash
docker run -d -p 8888:8888 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/notebooks:/app/notebooks \
  videogame-analysis \
  jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=''
```

Accede en: http://localhost:8888

---

## 🐳 Uso con Docker Compose

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

## 📊 Outputs Generados

Después de ejecutar el análisis, encontrarás en `output/`:

- **analisis_videojuegos.png** - Gráficas del análisis
- **Logs en consola** - Estadísticas y validación de hipótesis

---

## 🔧 Personalización

### **Modificar el script de análisis**

Edita `analisis_videojuegos.py` y los cambios se reflejarán automáticamente:

```bash
# Editar código
nano analisis_videojuegos.py

# Reconstruir y ejecutar
make build
make run
```

### **Agregar dependencias**

Edita `requirements.txt` y reconstruye:

```bash
# Agregar librería
echo "nueva-libreria==1.0.0" >> requirements.txt

# Reconstruir
make build
```

---

## 💡 Ventajas de Docker

✅ **No consume recursos locales** - Todo corre en contenedores aislados  
✅ **Portable** - Funciona igual en Windows, Mac, Linux  
✅ **Reproducible** - Mismo entorno siempre  
✅ **Fácil de compartir** - Solo necesitas Docker instalado  
✅ **Aislado** - No interfiere con tu sistema  

---

## 🆘 Solución de Problemas

### **Error: Dataset no encontrado**
```bash
# Verifica que vgsales.csv esté en data/
ls data/vgsales.csv
```

### **Error: Puerto 8888 ocupado**
```bash
# Cambiar puerto de Jupyter
docker run -p 8889:8888 ...
# Acceder en http://localhost:8889
```

### **Limpiar todo y empezar de nuevo**
```bash
make clean
make clean-output
make setup
make build
make run
```

---

## 📚 Requisitos

- **Docker** instalado ([Descargar aquí](https://www.docker.com/get-started))
- **Docker Compose** (incluido en Docker Desktop)
- **Make** (opcional, para comandos simplificados)
  - Linux/Mac: Viene preinstalado
  - Windows: Instalar con chocolatey `choco install make`

---

## 🎯 Próximos Pasos

1. ✅ Descargar dataset de Kaggle
2. ✅ Ejecutar `make setup`
3. ✅ Colocar CSV en `data/`
4. ✅ Ejecutar `make build`
5. ✅ Ejecutar `make run`
6. ✅ Revisar resultados en `output/`

---

## 📄 Licencia

Proyecto educativo - Mini Proyecto #01 de Curso de Python

---

## 👨‍💻 Autor

Estudiante de Python - Octubre 2025

---

**¿Preguntas?** Revisa la documentación o ejecuta `make help`