import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# --- INSTRUCCIONES ---
# Para que esta aplicación funcione, necesitas instalar algunas librerías de Python.
# Si no las tienes, abre una terminal o línea de comandos y ejecuta los siguientes comandos:
# 
# pip install pandas
# pip install matplotlib
# pip install seaborn
# 
# --------------------

class ConsumoApp(tk.Tk):
    """
    Aplicación de escritorio para visualizar y analizar datos de consumo eléctrico.
    """
    def __init__(self):
        super().__init__()
        self.title("Análisis de Consumo Eléctrico - Arequipa")
        self.geometry("1200x800")
        
        self.data_frame = None
        self.filtered_df = None

        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Panel de controles a la izquierda
        self.control_panel = ttk.LabelFrame(main_frame, text="Filtros y Controles", padding=10)
        self.control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # Panel de gráficos a la derecha
        self.plot_panel = ttk.Frame(main_frame)
        self.plot_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Notebook para mostrar los gráficos en pestañas
        self.plot_notebook = ttk.Notebook(self.plot_panel)
        self.plot_notebook.pack(fill=tk.BOTH, expand=True)

        self.load_data_and_create_widgets()

    def load_data_and_create_widgets(self):
        """
        Carga los datos del CSV y, si tiene éxito, crea los widgets de la interfaz.
        """
        csv_path = 'datos-consumo.csv'
        if not os.path.exists(csv_path):
            messagebox.showerror("Error de Archivo", f"No se encontró el archivo '{csv_path}'.\nAsegúrate de que el archivo esté en la misma carpeta que la aplicación.")
            self.destroy()
            return
            
        try:
            # Muestra un mensaje de carga
            loading_label = ttk.Label(self, text="Cargando datos, por favor espere...", font=("Helvetica", 14))
            loading_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.update()

            # Lectura robusta del CSV
            self.data_frame = pd.read_csv(
                csv_path,
                encoding='latin-1',   # Añadido para manejar errores de codificación UTF-8
                skipinitialspace=True,
                on_bad_lines='warn', # Advierte sobre líneas con errores pero las salta
                low_memory=False     # Recomendado para archivos grandes y evitar tipos mixtos
            )
            
            # Limpieza de nombres de columnas
            self.data_frame.columns = [col.strip() for col in self.data_frame.columns]

            # Conversión de datos numérica y robusta
            for col in ['ConsumoKwh', 'Facturado_Soles']:
                self.data_frame[col] = pd.to_numeric(self.data_frame[col], errors='coerce')
            
            # Rellenar valores que no se pudieron convertir (NaN) con 0
            self.data_frame.fillna({'ConsumoKwh': 0, 'Facturado_Soles': 0}, inplace=True)
            
            # Quitar el mensaje de carga
            loading_label.destroy()

        except Exception as e:
            messagebox.showerror("Error al Cargar Datos", f"Ocurrió un error inesperado al procesar el archivo CSV:\n{e}")
            self.destroy()
            return
        
        self.create_control_widgets()

    def create_control_widgets(self):
        """
        Crea los widgets del panel de control (filtros desplegables y botón).
        """
        # --- Filtro de Provincia ---
        ttk.Label(self.control_panel, text="Provincia:").pack(fill=tk.X, pady=(5,0))
        self.province_var = tk.StringVar(value="TODAS")
        provinces = ["TODAS"] + sorted(self.data_frame['NombreProvincia'].unique().tolist())
        self.province_combo = ttk.Combobox(self.control_panel, textvariable=self.province_var, values=provinces, state="readonly")
        self.province_combo.pack(fill=tk.X)
        self.province_combo.bind("<<ComboboxSelected>>", self.update_district_options)

        # --- Filtro de Distrito ---
        ttk.Label(self.control_panel, text="Distrito:").pack(fill=tk.X, pady=(10,0))
        self.district_var = tk.StringVar(value="TODOS")
        self.district_combo = ttk.Combobox(self.control_panel, textvariable=self.district_var, state="readonly")
        self.district_combo.pack(fill=tk.X)
        self.update_district_options() # Llenar con valores iniciales

        # --- Filtro de Tarifa ---
        ttk.Label(self.control_panel, text="Tarifa:").pack(fill=tk.X, pady=(10,0))
        self.tariff_var = tk.StringVar(value="TODAS")
        tariffs = ["TODAS"] + sorted(self.data_frame['Tarifa'].unique().tolist())
        self.tariff_combo = ttk.Combobox(self.control_panel, textvariable=self.tariff_var, values=tariffs, state="readonly")
        self.tariff_combo.pack(fill=tk.X)
        
        # --- Botón para generar gráficos ---
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 10, "bold"), padding=10)
        self.update_button = ttk.Button(self.control_panel, text="Generar Gráficos", command=self.apply_filters_and_plot, style="TButton")
        self.update_button.pack(fill=tk.X, pady=(20, 5))

    def update_district_options(self, event=None):
        """
        Actualiza las opciones del combobox de distritos según la provincia seleccionada.
        """
        selected_province = self.province_var.get()
        
        if selected_province == "TODAS":
            districts = ["TODOS"] + sorted(self.data_frame['NombreDistrito'].unique().tolist())
        else:
            districts = ["TODOS"] + sorted(self.data_frame[self.data_frame['NombreProvincia'] == selected_province]['NombreDistrito'].unique().tolist())
        
        self.district_combo['values'] = districts
        self.district_var.set("TODOS")

    def apply_filters_and_plot(self):
        """
        Aplica los filtros seleccionados al DataFrame y actualiza todos los gráficos.
        """
        province = self.province_var.get()
        district = self.district_var.get()
        tariff = self.tariff_var.get()

        self.filtered_df = self.data_frame.copy()

        if province != "TODAS":
            self.filtered_df = self.filtered_df[self.filtered_df['NombreProvincia'] == province]
        if district != "TODOS":
            self.filtered_df = self.filtered_df[self.filtered_df['NombreDistrito'] == district]
        if tariff != "TODAS":
            self.filtered_df = self.filtered_df[self.filtered_df['Tarifa'] == tariff]
        
        if self.filtered_df.empty:
            messagebox.showinfo("Sin Datos", "No se encontraron datos con los filtros seleccionados.")
            return

        # Limpiar pestañas anteriores
        for i in self.plot_notebook.tabs():
            self.plot_notebook.forget(i)

        # Generar y añadir cada gráfico en una nueva pestaña
        self.plot_bar_chart()
        self.plot_histogram()
        self.plot_scatter()
        self.plot_heatmap()

    def _create_plot_tab(self, title):
        """Helper para crear una nueva pestaña y un canvas para un gráfico."""
        tab = ttk.Frame(self.plot_notebook)
        self.plot_notebook.add(tab, text=title)
        fig, ax = plt.subplots(figsize=(10, 7), tight_layout=True)
        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        return fig, ax, canvas
        
    def plot_bar_chart(self):
        """Gráfico de barras del consumo total por distrito."""
        fig, ax, canvas = self._create_plot_tab("Consumo por Distrito")
        
        if self.filtered_df.empty:
            return

        # Agrupar por distrito y sumar el consumo
        consumption_by_district = self.filtered_df.groupby('NombreDistrito')['ConsumoKwh'].sum().nlargest(20).sort_values()

        if consumption_by_district.empty:
            ax.text(0.5, 0.5, "No hay datos suficientes para este gráfico.", ha='center', va='center')
        else:
            consumption_by_district.plot(kind='barh', ax=ax, color='skyblue')
            ax.set_title("Top 20 Consumo Total (Kwh) por Distrito")
            ax.set_xlabel("Consumo Total (Kwh)")
            ax.set_ylabel("Distrito")
            # Formatear etiquetas para que sean legibles
            ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))

        canvas.draw()
        
    def plot_histogram(self):
        """Histograma de la distribución del consumo."""
        fig, ax, canvas = self._create_plot_tab("Distribución de Consumo")

        # Filtrar consumos muy altos para una mejor visualización del grueso de los datos
        plot_data = self.filtered_df[self.filtered_df['ConsumoKwh'] <= self.filtered_df['ConsumoKwh'].quantile(0.95)]
        
        if plot_data.empty:
            ax.text(0.5, 0.5, "No hay datos suficientes para este gráfico.", ha='center', va='center')
        else:
            sns.histplot(plot_data['ConsumoKwh'], bins=50, kde=True, ax=ax)
            ax.set_title("Distribución del Consumo (Kwh) - Hasta el Percentil 95")
            ax.set_xlabel("Consumo (Kwh)")
            ax.set_ylabel("Frecuencia")
        
        canvas.draw()

    def plot_scatter(self):
        """Gráfico de dispersión de Consumo vs. Facturación."""
        fig, ax, canvas = self._create_plot_tab("Consumo vs. Facturación")
        
        # Usar una muestra para evitar sobrecarga en el gráfico si hay muchos puntos
        sample_df = self.filtered_df.sample(n=min(5000, len(self.filtered_df)))
        
        if sample_df.empty:
            ax.text(0.5, 0.5, "No hay datos suficientes para este gráfico.", ha='center', va='center')
        else:
            sns.scatterplot(data=sample_df, x='ConsumoKwh', y='Facturado_Soles', hue='Tarifa', alpha=0.6, ax=ax)
            ax.set_title("Consumo (Kwh) vs. Facturado (Soles)")
            ax.set_xlabel("Consumo (Kwh)")
            ax.set_ylabel("Facturado (Soles)")
            ax.legend(title="Tarifa")
            # Formatear ejes
            ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))

        canvas.draw()
        
    def plot_heatmap(self):
        """Mapa de calor del consumo promedio por distrito y tarifa."""
        fig, ax, canvas = self._create_plot_tab("Mapa de Calor (Consumo Promedio)")
        
        if self.filtered_df.empty or 'NombreDistrito' not in self.filtered_df or 'Tarifa' not in self.filtered_df:
             return

        # Crear una tabla pivote
        try:
            # Tomar los 20 distritos con más registros para que el mapa no sea muy grande
            top_districts = self.filtered_df['NombreDistrito'].value_counts().nlargest(20).index
            heatmap_data = self.filtered_df[self.filtered_df['NombreDistrito'].isin(top_districts)]

            pivot_table = heatmap_data.pivot_table(values='ConsumoKwh', index='NombreDistrito', columns='Tarifa', aggfunc='mean')
            
            if pivot_table.empty:
                ax.text(0.5, 0.5, "No hay datos suficientes para el mapa de calor.", ha='center', va='center')
            else:
                sns.heatmap(pivot_table, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax, linewidths=.5)
                ax.set_title("Consumo Promedio (Kwh) por Distrito y Tarifa")
                ax.set_xlabel("Tarifa")
                ax.set_ylabel("Distrito")
                plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

        except Exception as e:
            ax.text(0.5, 0.5, f"No se pudo generar el mapa de calor.\nError: {e}", ha='center', va='center')
        
        canvas.draw()


if __name__ == "__main__":
    app = ConsumoApp()
    app.mainloop()
