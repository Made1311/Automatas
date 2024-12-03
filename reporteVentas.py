import tkinter as tk
from conexion import conectar_bd
from tkinter import messagebox, ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import sqlite3 
from fpdf import FPDF
import os

# Función para obtener ventas filtradas usando el procedimiento almacenado
def obtener_ventas_filtradas(dia, mes, semana, empleado):
    # Conectar a la base de datos
    conexion = conectar_bd()
    cursor = conexion.cursor()
    
    try:
        # Llamar al procedimiento almacenado
        cursor.callproc('FiltrarVentas', [dia if dia else None, 
                                          mes if mes else None, 
                                          semana if semana else None, 
                                          empleado if empleado else None])
        
        # Recuperar resultados
        ventas = cursor.fetchall()
    except Exception as e:
        print(f"Error al ejecutar el procedimiento almacenado: {e}")
        ventas = []
    finally:
        # Cerrar la conexión
        conexion.close()

    return ventas
# Función para obtener el número consecutivo
def obtener_numero_consecutivo():
    archivo_contador = "contador_reporte.txt"
    
    # Si el archivo no existe, lo creamos con un valor inicial de 1
    if not os.path.exists(archivo_contador):
        with open(archivo_contador, "w") as archivo:
            archivo.write("1")
        return 1

    # Leer el número actual del archivo
    with open(archivo_contador, "r") as archivo:
        numero = int(archivo.read().strip())

    # Incrementar el número y guardarlo de nuevo
    with open(archivo_contador, "w") as archivo:
        archivo.write(str(numero + 1))

    return numero
# Función para crear el reporte PDF
def generar_reporte_pdf(ventas, filtro_dia, filtro_mes, filtro_semana, filtro_empleado):
    # Crear un archivo PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    
    # Título del PDF
    pdf.set_text_color(0, 0, 0)  
    pdf.cell(200, 10, txt="Reporte de Ventas", ln=True, align="C")
    pdf.ln(10)

    # Encabezado de la tabla
    pdf.set_fill_color(206, 216, 254) 
    pdf.set_text_color(0, 0, 0)  
    pdf.set_font("Arial", "B", 8)
    headers = ["ID", "Fecha", "Empleado", "Cliente", "Productos", "Total", "Tipo de Pago"]
    widths = [10, 30, 30, 30, 40, 20, 30]
    for header, width in zip(headers, widths):
        pdf.cell(width, 10, header, 1, 0, 'C')
    pdf.ln()
      # Obtener el número consecutivo para el archivo
    numero_consecutivo = obtener_numero_consecutivo()
    # Mostrar las ventas
    pdf.set_font("Arial", "", 8)
    for venta in ventas:
        for i, value in enumerate(venta):
            pdf.cell(widths[i], 10, str(value)[:widths[i] - 2], 1)
        pdf.ln()        

    pdf_file_path = f"ReporteVentas_{numero_consecutivo}_{datetime.now().strftime('%Y%m%d')}.pdf"
    pdf.output(pdf_file_path)
    print(f"Reporte generado: {pdf_file_path}")

# Obtener lista de empleados
def obtener_empleados():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT nombre FROM usuarios")
        empleados = [empleado[0] for empleado in cursor.fetchall()]
    except Exception as e:
        print(f"Error al obtener empleados: {e}")
        empleados = []
    finally:
        conexion.close()
    return empleados

# Ventana de reportes
def ventanaReportesVentas(root):
    ventana_reporteVentas = tk.Toplevel(root)
    ventana_reporteVentas.title("Reporte de ventas")
    ventana_reporteVentas.geometry("300x400")
    
    # Centrar ventana
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (300 // 2)
    y = (screen_height // 2) - (400 // 2)
    ventana_reporteVentas.geometry(f"300x400+{x}+{y}")
    
    # Filtros
    tk.Label(ventana_reporteVentas, text="Filtrar por Día").pack(pady=5)
    dia = ttk.Combobox(ventana_reporteVentas, values=list(range(1, 32)), state="readonly")
    dia.pack(pady=5)

    tk.Label(ventana_reporteVentas, text="Filtrar por Mes").pack(pady=5)
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    mes = ttk.Combobox(ventana_reporteVentas, values=meses, state="readonly")
    mes.pack(pady=5)

    tk.Label(ventana_reporteVentas, text="Filtrar por Semana").pack(pady=5)
    semana = ttk.Combobox(ventana_reporteVentas, values=list(range(1, 53)), state="readonly")
    semana.pack(pady=5)

    tk.Label(ventana_reporteVentas, text="Empleado").pack(pady=5)
    empleados = obtener_empleados()
    combo_empleado = ttk.Combobox(ventana_reporteVentas, values=empleados, state="readonly")
    combo_empleado.pack(pady=5)
    
    def aplicar_filtro():
        filtro_dia = dia.get()
        filtro_mes = mes.get()
        filtro_semana = semana.get()
        filtro_empleado = combo_empleado.get()

        # Convertir entradas vacías a None
        filtro_dia = int(filtro_dia) if filtro_dia else None
        filtro_mes = str(filtro_mes) if filtro_mes else None
        filtro_empleado = str(filtro_empleado) if filtro_empleado else None
        filtro_semana = int(filtro_semana) if filtro_semana else None

        # Obtener ventas
        ventas = obtener_ventas_filtradas(filtro_dia, filtro_mes, filtro_semana, filtro_empleado)
        
        if ventas:
            generar_reporte_pdf(ventas, filtro_dia, filtro_mes, filtro_semana, filtro_empleado)
            messagebox.showinfo("Éxito", "Reporte generado con éxito.")
        else:
            messagebox.showwarning("Sin datos", "No se encontraron ventas con los filtros aplicados.")

    tk.Button(ventana_reporteVentas, text="Crear reporte", command=aplicar_filtro).pack(pady=20)