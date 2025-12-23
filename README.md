# Análisis Estadístico de Consumo Eléctrico - Arequipa

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue?style=flat&logo=github)](https://github.com/Suarezsh/Analisis-estadistico-electrico/)
[![Live Demo](https://img.shields.io/badge/Live-Demo-green?style=flat&logo=github)](https://suarezsh.github.io/Analisis-estadistico-electrico/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Descripción

Esta aplicación web permite realizar un análisis estadístico detallado del consumo eléctrico en la región de Arequipa, Perú. Facilita la carga de datos en formato CSV, la aplicación de filtros por provincia, distrito y tarifa, y la generación de estadísticas descriptivas junto con visualizaciones interactivas como histogramas, diagramas de caja, gráficos de barras, dispersiones y mapas de calor.

El proyecto está diseñado para ser intuitivo y eficiente, procesando grandes volúmenes de datos de manera óptima para ofrecer insights valiosos sobre patrones de consumo energético.

## Características Principales

- **Carga de Datos CSV**: Soporte para archivos CSV con columnas específicas (Código de Suministro, Período Facturado, Consumo en KWh, Facturado en Soles, Fecha de Emisión, Ubigeo, Provincia, Distrito, Departamento, Tarifa).
- **Filtros Dinámicos**: Selección interactiva de provincia, distrito y tarifa para segmentar los datos.
- **Estadísticas Descriptivas**: Cálculo automático de métricas como media, mediana, desviación estándar, totales y más.
- **Visualizaciones Interactivas**:
  - Histograma de distribución de consumo.
  - Diagrama de caja (boxplot) por tarifa.
  - Gráfico de barras del consumo total por distrito (top 10).
  - Gráfico de dispersión entre consumo y facturación.
  - Mapa de calor del consumo promedio por distrito y tarifa.
- **Procesamiento Eficiente**: Manejo de datos grandes mediante procesamiento en chunks para evitar bloqueos del navegador.
- **Diseño Responsivo**: Interfaz adaptativa que funciona en dispositivos móviles y de escritorio.
- **Interfaz en Español**: Toda la aplicación está localizada en español para mayor accesibilidad.

## Tecnologías Utilizadas

Este proyecto utiliza una combinación de tecnologías modernas para el frontend y la visualización de datos:

| Tecnología | Descripción |
|------------|-------------|
| **HTML5** | Lenguaje de marcado para estructurar el contenido web. |
| **CSS3** | Lenguaje de estilos para el diseño y presentación. |
| **JavaScript** | Lenguaje de programación para la lógica interactiva. |
| **Bootstrap 5** | Framework CSS para diseño responsivo y componentes UI. |
| **Font Awesome** | Biblioteca de iconos vectoriales escalables. |
| **ApexCharts** | Librería para gráficos interactivos (histogramas, barras, dispersiones). |
| **Plotly.js** | Librería para visualizaciones avanzadas (boxplots, mapas de calor). |
| **PapaParse** | Librería para parseo eficiente de archivos CSV. |
| **D3.js** | Librería para manipulación y visualización de datos. |

## Instalación

### Prerrequisitos

- Un navegador web moderno (Chrome, Firefox, Safari, Edge) con soporte para JavaScript habilitado.
- Conexión a internet para cargar las librerías externas (Bootstrap, ApexCharts, Plotly, etc.).

### Pasos de Instalación

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/Suarezsh/Analisis-estadistico-electrico.git
   cd Analisis-estadistico-electrico
   ```

2. **Abre el archivo**:
   - Abre `index.html` directamente en tu navegador web.
   - No se requieren dependencias adicionales ya que todas las librerías se cargan desde CDNs.

3. **Ejecución Local**:
   - Si deseas ejecutar en un servidor local (opcional para evitar restricciones de CORS en algunos navegadores), usa:
     ```bash
     python -m http.server 8000
     ```
     O con Node.js:
     ```bash
     npx http-server
     ```
   - Accede a `http://localhost:8000/index.html`.

## Uso

1. **Carga de Datos**:
   - Haz clic en "Subir Archivo CSV" y selecciona un archivo CSV válido con las columnas requeridas.

2. **Aplicar Filtros**:
   - Selecciona opciones en Provincia, Distrito y Tarifa.
   - Haz clic en "Aplicar Filtros y Generar Análisis".

3. **Visualización de Resultados**:
   - Revisa las estadísticas descriptivas en la tabla.
   - Explora los gráficos interactivos generados.

4. **Interacción con Gráficos**:
   - Usa zoom, pan y tooltips en los gráficos de ApexCharts y Plotly para profundizar en los datos.

### Formato de Datos CSV

El archivo CSV debe contener las siguientes columnas obligatorias:
- `CodigoSuministro`: Código único del suministro.
- `PeriodoFacturado`: Período del facturado (ej. mes/año).
- `ConsumoKwh`: Consumo en kilovatios-hora (numérico).
- `Facturado_Soles`: Monto facturado en soles (numérico).
- `FechaEmisionRecibo`: Fecha de emisión del recibo.
- `CodigoUbigeo`: Código ubigeo del distrito.
- `NombreProvincia`: Nombre de la provincia.
- `NombreDistrito`: Nombre del distrito.
- `NombreDepartamento`: Nombre del departamento.
- `Tarifa`: Tipo de tarifa aplicada.

Ejemplo de fila:
```
CodigoSuministro,PeriodoFacturado,ConsumoKwh,Facturado_Soles,FechaEmisionRecibo,CodigoUbigeo,NombreProvincia,NombreDistrito,NombreDepartamento,Tarifa
12345,2023-01,150.5,200.75,2023-01-15,040101,Arequipa,Arequipa,Arequipa,BT5B
```

## Contribución

¡Las contribuciones son bienvenidas! Para contribuir:

1. Fork el repositorio.
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y confirma (`git commit -m 'Agrega nueva funcionalidad'`).
4. Push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

### Guías de Contribución

- Sigue las mejores prácticas de HTML/CSS/JS.
- Asegura compatibilidad con navegadores modernos.
- Prueba cambios con datos de muestra.
- Mantén la documentación actualizada.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

<div align="center">

**Hecho con ❤️ para promover el análisis de datos energéticos en Perú.**

</div></content>
<parameter name="filePath">C:\xampp1\htdocs\Github\EMAT-TIF\README.md
