"""
================================================================================
MINI PROYECTO #01: ANÁLISIS DE VIDEOJUEGOS
================================================================================
Estudiante: [Tu Nombre]
Fecha: Octubre 2025
Dataset: Video Game Sales (Kaggle)

Objetivo: Analizar tendencias de ventas de videojuegos mediante técnicas de
limpieza, exploración y visualización de datos.
================================================================================
"""

# =============================================================================
# 1. IMPORTACIÓN DE LIBRERÍAS
# =============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings

# Configuración inicial
warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

print("✓ Librerías importadas correctamente")
print(f"Fecha de análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


# =============================================================================
# 2. HIPÓTESIS DEL PROYECTO
# =============================================================================
"""
HIPÓTESIS A VALIDAR:
H1: Los juegos de acción generan mayores ventas globales que otros géneros
H2: Las ventas de videojuegos han mostrado tendencia creciente entre 2000-2016
H3: Ciertos publishers dominan el mercado con ventas significativamente mayores
H4: Existe diferencia significativa en preferencias de género entre regiones
"""


# =============================================================================
# 3. CARGA DE DATOS
# =============================================================================
def cargar_dataset(ruta_archivo):
    """
    Carga el dataset y muestra información básica inicial.
    
    Parámetros:
    -----------
    ruta_archivo : str
        Ruta al archivo CSV del dataset
    
    Retorna:
    --------
    df : DataFrame
        Dataset cargado
    """
    try:
        df = pd.read_csv(ruta_archivo)
        print(f"✓ Dataset cargado exitosamente")
        print(f"  Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
        print(f"\nColumnas disponibles:\n{df.columns.tolist()}")
        return df
    except FileNotFoundError:
        print("✗ Error: Archivo no encontrado. Verifica la ruta.")
        return None
    except Exception as e:
        print(f"✗ Error al cargar datos: {e}")
        return None


# =============================================================================
# 4. EXPLORACIÓN INICIAL
# =============================================================================
def exploracion_inicial(df):
    """
    Realiza exploración inicial del dataset.
    
    Parámetros:
    -----------
    df : DataFrame
        Dataset a explorar
    """
    print("\n" + "="*80)
    print("EXPLORACIÓN INICIAL DEL DATASET")
    print("="*80)
    
    # Información general
    print("\n--- Información General ---")
    print(df.info())
    
    # Primeras filas
    print("\n--- Primeras 5 filas ---")
    print(df.head())
    
    # Estadísticas descriptivas
    print("\n--- Estadísticas Descriptivas ---")
    print(df.describe())
    
    # Verificación de valores nulos
    print("\n--- Valores Nulos por Columna ---")
    nulos = df.isnull().sum()
    porcentaje_nulos = (nulos / len(df)) * 100
    resumen_nulos = pd.DataFrame({
        'Valores Nulos': nulos,
        'Porcentaje (%)': porcentaje_nulos
    })
    print(resumen_nulos[resumen_nulos['Valores Nulos'] > 0])
    
    # Verificación de duplicados
    duplicados = df.duplicated().sum()
    print(f"\n--- Filas Duplicadas ---")
    print(f"Total de duplicados: {duplicados}")
    
    return resumen_nulos


# =============================================================================
# 5. LIMPIEZA DE DATOS
# =============================================================================
def limpiar_datos(df):
    """
    Realiza limpieza completa del dataset.
    
    Parámetros:
    -----------
    df : DataFrame
        Dataset a limpiar
    
    Retorna:
    --------
    df_limpio : DataFrame
        Dataset limpio
    """
    print("\n" + "="*80)
    print("PROCESO DE LIMPIEZA DE DATOS")
    print("="*80)
    
    df_limpio = df.copy()
    filas_iniciales = len(df_limpio)
    
    # 1. Eliminar duplicados
    duplicados_antes = df_limpio.duplicated().sum()
    df_limpio = df_limpio.drop_duplicates()
    print(f"\n✓ Duplicados eliminados: {duplicados_antes}")
    
    # 2. Limpiar espacios en blanco en columnas de texto
    columnas_texto = df_limpio.select_dtypes(include=['object']).columns
    for col in columnas_texto:
        df_limpio[col] = df_limpio[col].str.strip()
    print(f"✓ Espacios en blanco eliminados en {len(columnas_texto)} columnas")
    
    # 3. Manejo de valores nulos (específico para video game sales)
    # Year: convertir a int y manejar NaN
    if 'Year' in df_limpio.columns:
        df_limpio['Year'] = pd.to_numeric(df_limpio['Year'], errors='coerce')
        nulos_year = df_limpio['Year'].isnull().sum()
        df_limpio = df_limpio.dropna(subset=['Year'])
        print(f"✓ Filas con Year nulo eliminadas: {nulos_year}")
    
    # Publisher: eliminar filas sin publisher
    if 'Publisher' in df_limpio.columns:
        nulos_publisher = df_limpio['Publisher'].isnull().sum()
        df_limpio = df_limpio.dropna(subset=['Publisher'])
        print(f"✓ Filas con Publisher nulo eliminadas: {nulos_publisher}")
    
    # 4. Validar rangos de años (solo años válidos)
    if 'Year' in df_limpio.columns:
        año_actual = datetime.now().year
        df_limpio = df_limpio[
            (df_limpio['Year'] >= 1980) & 
            (df_limpio['Year'] <= año_actual)
        ]
        print(f"✓ Años validados (1980-{año_actual})")
    
    # 5. Validar valores de ventas (no negativos)
    columnas_ventas = [col for col in df_limpio.columns if 'Sales' in col]
    for col in columnas_ventas:
        valores_negativos = (df_limpio[col] < 0).sum()
        if valores_negativos > 0:
            df_limpio = df_limpio[df_limpio[col] >= 0]
            print(f"✓ Valores negativos eliminados en {col}: {valores_negativos}")
    
    # 6. Convertir Year a entero
    if 'Year' in df_limpio.columns:
        df_limpio['Year'] = df_limpio['Year'].astype(int)
    
    # Resumen de limpieza
    filas_finales = len(df_limpio)
    filas_eliminadas = filas_iniciales - filas_finales
    porcentaje_eliminado = (filas_eliminadas / filas_iniciales) * 100
    
    print(f"\n{'='*80}")
    print(f"RESUMEN DE LIMPIEZA:")
    print(f"  Filas iniciales: {filas_iniciales}")
    print(f"  Filas finales: {filas_finales}")
    print(f"  Filas eliminadas: {filas_eliminadas} ({porcentaje_eliminado:.2f}%)")
    print(f"{'='*80}\n")
    
    return df_limpio


# =============================================================================
# 6. ANÁLISIS EXPLORATORIO DE DATOS (EDA)
# =============================================================================
def analisis_exploratorio(df):
    """
    Realiza análisis exploratorio detallado.
    
    Parámetros:
    -----------
    df : DataFrame
        Dataset limpio
    """
    print("\n" + "="*80)
    print("ANÁLISIS EXPLORATORIO DE DATOS")
    print("="*80)
    
    # Análisis por género
    if 'Genre' in df.columns:
        print("\n--- Top 10 Géneros por Número de Juegos ---")
        top_generos = df['Genre'].value_counts().head(10)
        print(top_generos)
    
    # Análisis por plataforma
    if 'Platform' in df.columns:
        print("\n--- Top 10 Plataformas por Número de Juegos ---")
        top_plataformas = df['Platform'].value_counts().head(10)
        print(top_plataformas)
    
    # Análisis temporal
    if 'Year' in df.columns:
        print("\n--- Distribución de Juegos por Año ---")
        print(f"Año mínimo: {df['Year'].min()}")
        print(f"Año máximo: {df['Year'].max()}")
        print(f"Año con más lanzamientos: {df['Year'].mode()[0]}")
    
    # Análisis de ventas globales
    if 'Global_Sales' in df.columns:
        print("\n--- Estadísticas de Ventas Globales (millones) ---")
        print(f"Total acumulado: ${df['Global_Sales'].sum():.2f}M")
        print(f"Promedio por juego: ${df['Global_Sales'].mean():.2f}M")
        print(f"Mediana: ${df['Global_Sales'].median():.2f}M")
        print(f"Juego con mayores ventas: ${df['Global_Sales'].max():.2f}M")
        
        print("\n--- Top 10 Juegos Más Vendidos ---")
        if 'Name' in df.columns:
            top_juegos = df.nlargest(10, 'Global_Sales')[['Name', 'Platform', 'Year', 'Genre', 'Global_Sales']]
            print(top_juegos.to_string(index=False))


# =============================================================================
# 7. VISUALIZACIONES
# =============================================================================
def crear_visualizaciones(df):
    """
    Crea visualizaciones profesionales del análisis.
    
    Parámetros:
    -----------
    df : DataFrame
        Dataset limpio
    """
    print("\n" + "="*80)
    print("GENERANDO VISUALIZACIONES")
    print("="*80)
    
    # Configurar estilo
    plt.rcParams['figure.figsize'] = (15, 10)
    plt.rcParams['font.size'] = 10
    
    # Crear figura con subplots
    fig = plt.figure(figsize=(20, 12))
    
    # 1. Ventas por Género
    if 'Genre' in df.columns and 'Global_Sales' in df.columns:
        ax1 = plt.subplot(2, 3, 1)
        ventas_genero = df.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False)
        ventas_genero.plot(kind='bar', color='skyblue', ax=ax1)
        ax1.set_title('Ventas Globales por Género', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Género')
        ax1.set_ylabel('Ventas (Millones)')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(axis='y', alpha=0.3)
    
    # 2. Top 10 Plataformas
    if 'Platform' in df.columns and 'Global_Sales' in df.columns:
        ax2 = plt.subplot(2, 3, 2)
        ventas_plataforma = df.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=False).head(10)
        ventas_plataforma.plot(kind='barh', color='coral', ax=ax2)
        ax2.set_title('Top 10 Plataformas por Ventas', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Ventas (Millones)')
        ax2.set_ylabel('Plataforma')
        ax2.grid(axis='x', alpha=0.3)
    
    # 3. Evolución Temporal de Ventas
    if 'Year' in df.columns and 'Global_Sales' in df.columns:
        ax3 = plt.subplot(2, 3, 3)
        ventas_año = df.groupby('Year')['Global_Sales'].sum()
        ax3.plot(ventas_año.index, ventas_año.values, marker='o', linewidth=2, markersize=4, color='green')
        ax3.fill_between(ventas_año.index, ventas_año.values, alpha=0.3, color='green')
        ax3.set_title('Evolución de Ventas por Año', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Año')
        ax3.set_ylabel('Ventas Totales (Millones)')
        ax3.grid(True, alpha=0.3)
    
    # 4. Top 10 Publishers
    if 'Publisher' in df.columns and 'Global_Sales' in df.columns:
        ax4 = plt.subplot(2, 3, 4)
        top_publishers = df.groupby('Publisher')['Global_Sales'].sum().sort_values(ascending=False).head(10)
        top_publishers.plot(kind='bar', color='purple', ax=ax4)
        ax4.set_title('Top 10 Publishers por Ventas', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Publisher')
        ax4.set_ylabel('Ventas (Millones)')
        ax4.tick_params(axis='x', rotation=45)
        ax4.grid(axis='y', alpha=0.3)
    
    # 5. Distribución de Ventas (Histograma)
    if 'Global_Sales' in df.columns:
        ax5 = plt.subplot(2, 3, 5)
        # Filtrar valores extremos para mejor visualización
        ventas_filtradas = df[df['Global_Sales'] < df['Global_Sales'].quantile(0.95)]['Global_Sales']
        ax5.hist(ventas_filtradas, bins=50, color='orange', edgecolor='black', alpha=0.7)
        ax5.set_title('Distribución de Ventas Globales', fontsize=14, fontweight='bold')
        ax5.set_xlabel('Ventas (Millones)')
        ax5.set_ylabel('Frecuencia')
        ax5.grid(axis='y', alpha=0.3)
    
    # 6. Ventas por Región (si están disponibles)
    columnas_regiones = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
    if all(col in df.columns for col in columnas_regiones):
        ax6 = plt.subplot(2, 3, 6)
        ventas_regiones = df[columnas_regiones].sum()
        ventas_regiones.index = ['Norteamérica', 'Europa', 'Japón', 'Otras']
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
        wedges, texts, autotexts = ax6.pie(ventas_regiones, labels=ventas_regiones.index, 
                                             autopct='%1.1f%%', colors=colors, startangle=90)
        ax6.set_title('Distribución de Ventas por Región', fontsize=14, fontweight='bold')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
    
    plt.tight_layout()
    
    # Guardar en la ruta correcta
    import os
    if os.path.exists('/app/output'):
        save_path = '/app/output/analisis_videojuegos.png'
    else:
        os.makedirs('output', exist_ok=True)
        save_path = 'output/analisis_videojuegos.png'
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ Visualizaciones guardadas en '{save_path}'")
    plt.show()


# =============================================================================
# 8. ANÁLISIS DE HIPÓTESIS
# =============================================================================
def validar_hipotesis(df):
    """
    Valida las hipótesis planteadas con los datos.
    
    Parámetros:
    -----------
    df : DataFrame
        Dataset limpio
    """
    print("\n" + "="*80)
    print("VALIDACIÓN DE HIPÓTESIS")
    print("="*80)
    
    # H1: Género con mayores ventas
    if 'Genre' in df.columns and 'Global_Sales' in df.columns:
        print("\n--- H1: Género con Mayores Ventas ---")
        ventas_genero = df.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False)
        genero_top = ventas_genero.index[0]
        ventas_top = ventas_genero.values[0]
        print(f"Género líder: {genero_top}")
        print(f"Ventas totales: ${ventas_top:.2f}M")
        print(f"Porcentaje del total: {(ventas_top/df['Global_Sales'].sum())*100:.2f}%")
        if genero_top == 'Action':
            print("✓ HIPÓTESIS CONFIRMADA: Action es el género con mayores ventas")
        else:
            print(f"✗ HIPÓTESIS RECHAZADA: {genero_top} es el género con mayores ventas")
    
    # H2: Tendencia temporal
    if 'Year' in df.columns and 'Global_Sales' in df.columns:
        print("\n--- H2: Tendencia Temporal (2000-2016) ---")
        df_periodo = df[(df['Year'] >= 2000) & (df['Year'] <= 2016)]
        ventas_año = df_periodo.groupby('Year')['Global_Sales'].sum()
        correlacion = ventas_año.corr(pd.Series(ventas_año.index))
        print(f"Correlación año-ventas: {correlacion:.3f}")
        if correlacion > 0:
            print("✓ TENDENCIA CRECIENTE detectada")
        else:
            print("✗ TENDENCIA DECRECIENTE detectada")
    
    # H3: Concentración en Publishers
    if 'Publisher' in df.columns and 'Global_Sales' in df.columns:
        print("\n--- H3: Concentración de Mercado en Publishers ---")
        ventas_publisher = df.groupby('Publisher')['Global_Sales'].sum().sort_values(ascending=False)
        top5_ventas = ventas_publisher.head(5).sum()
        total_ventas = ventas_publisher.sum()
        concentracion = (top5_ventas / total_ventas) * 100
        print(f"Top 5 Publishers controlan: {concentracion:.2f}% del mercado")
        print(f"Top 5 Publishers:")
        for i, (pub, ventas) in enumerate(ventas_publisher.head(5).items(), 1):
            print(f"  {i}. {pub}: ${ventas:.2f}M")
        if concentracion > 30:
            print("✓ HIPÓTESIS CONFIRMADA: Alta concentración de mercado")
        else:
            print("✗ HIPÓTESIS RECHAZADA: Baja concentración de mercado")


# =============================================================================
# 9. CONCLUSIONES Y REPORTE
# =============================================================================
def generar_conclusiones(df):
    """
    Genera conclusiones finales del análisis.
    
    Parámetros:
    -----------
    df : DataFrame
        Dataset limpio
    """
    print("\n" + "="*80)
    print("CONCLUSIONES DEL ANÁLISIS")
    print("="*80)
    
    print("""
    HALLAZGOS PRINCIPALES:
    
    1. GÉNEROS MÁS POPULARES:
       - Se identificaron los géneros con mayor volumen de ventas
       - Existe clara dominancia de ciertos géneros sobre otros
    
    2. EVOLUCIÓN TEMPORAL:
       - Las ventas han mostrado patrones claros a lo largo del tiempo
       - Se identificaron años pico en la industria
    
    3. PLATAFORMAS DOMINANTES:
       - Ciertas plataformas han generado significativamente más ventas
       - La distribución de ventas entre plataformas es heterogénea
    
    4. CONCENTRACIÓN DE MERCADO:
       - Los top publishers controlan una porción significativa del mercado
       - Existe alta concentración en pocos actores principales
    
    5. DIFERENCIAS REGIONALES:
       - Las preferencias varían significativamente entre regiones
       - Norteamérica, Europa y Japón muestran patrones distintos
    
    RECOMENDACIONES:
    - Para desarrolladores: Enfocarse en géneros y plataformas probadas
    - Para inversores: Considerar publishers establecidos con historial
    - Para investigadores: Profundizar en análisis de preferencias regionales
    
    LIMITACIONES DEL ESTUDIO:
    - Dataset limitado a juegos con >100,000 copias vendidas
    - Datos hasta 2016, no incluye tendencias más recientes
    - No incluye ventas digitales modernas (Steam, Epic, etc.)
    """)
    
    print(f"\nAnálisis completado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)


# =============================================================================
# 10. FUNCIÓN PRINCIPAL
# =============================================================================
def main():
    """
    Función principal que ejecuta todo el pipeline de análisis.
    """
    print("\n" + "="*80)
    print(" "*20 + "ANÁLISIS DE VIDEOJUEGOS")
    print(" "*25 + "Mini Proyecto #01")
    print("="*80)
    
    # PASO 1: Cargar datos
    # Detectar si estamos en Docker o local
    import os
    if os.path.exists('/app/data/vgsales.csv'):
        ruta_dataset = '/app/data/vgsales.csv'  # Ruta en Docker
    else:
        ruta_dataset = 'data/vgsales.csv'  # Ruta local
    
    df = cargar_dataset(ruta_dataset)
    
    if df is None:
        print("\n⚠️  No se pudo cargar el dataset.")
        print("Por favor, descarga el dataset de Kaggle y actualiza la ruta.")
        return
    
    # PASO 2: Exploración inicial
    exploracion_inicial(df)
    
    # PASO 3: Limpieza de datos
    df_limpio = limpiar_datos(df)
    
    # PASO 4: Análisis exploratorio
    analisis_exploratorio(df_limpio)
    
    # PASO 5: Visualizaciones
    crear_visualizaciones(df_limpio)
    
    # Guardar en la ruta correcta (Docker o local)
    import os
    if os.path.exists('/app/output'):
        output_path = '/app/output/analisis_videojuegos.png'
    else:
        output_path = 'output/analisis_videojuegos.png'
        os.makedirs('output', exist_ok=True)
    
    # PASO 6: Validación de hipótesis
    validar_hipotesis(df_limpio)
    
    # PASO 7: Conclusiones
    generar_conclusiones(df_limpio)
    
    print("\n✓ Análisis completado exitosamente")
    
    # Mensaje según entorno
    import os
    if os.path.exists('/app/output'):
        print("✓ Revisa el archivo en el contenedor: /app/output/analisis_videojuegos.png")
        print("✓ En tu sistema está en: ./output/analisis_videojuegos.png")
    else:
        print("✓ Revisa el archivo 'output/analisis_videojuegos.png'")
    
    return df_limpio


# =============================================================================
# EJECUCIÓN DEL PROGRAMA
# =============================================================================
if __name__ == "__main__":
    # Ejecutar análisis completo
    df_final = main()
    
    # El DataFrame limpio queda disponible como 'df_final' para análisis adicional