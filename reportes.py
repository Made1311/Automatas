import tkinter as tk
import random
from tkinter import messagebox, ttk
from conexion import conectar_bd  # Importa la función de conexión
from reporteVentas import ventanaReportesVentas
import mysql.connector
from datetime import datetime
from reportlab.lib.pagesizes import letter
from fpdf import FPDF
import os

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

# Función para generar el reporte de productos
def generar_reporte_productos():
    try:
        # Conexión a la base de datos
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        # Consulta para obtener los datos de la tabla productos
        cursor.execute("SELECT codBarras, nombre, cantidad, proveedores, especificaciones, fechaCad, costoCompra, costoVenta FROM productos")
        productos = cursor.fetchall()
        
        if not productos:
            messagebox.showinfo("Sin datos", "No hay productos registrados para generar el reporte.")
            return
        # Obtener el número consecutivo para el archivo
        numero_consecutivo = obtener_numero_consecutivo()
        # Crear el PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        
        # Título del PDF
        pdf.set_text_color(0, 0, 0)  
        pdf.cell(200, 10, txt="Reporte de Productos", ln=True, align="C")
        pdf.ln(10)
        
        # Encabezado de la tabla
        pdf.set_fill_color(206, 216, 254) 
        pdf.set_text_color(0, 0, 0)  
        pdf.set_font("Arial", "B", 8)
        pdf.cell(20, 10, "Código", 1)
        pdf.cell(30, 10, "Nombre", 1)
        pdf.cell(15, 10, "Cantidad", 1)
        pdf.cell(30, 10, "Proveedor", 1)
        pdf.cell(30, 10, "Especificaciones", 1)
        pdf.cell(20, 10, "Fecha Cad.", 1)
        pdf.cell(20, 10, "C. Compra", 1)
        pdf.cell(20, 10, "C. Venta", 1)
        pdf.ln()
        
        # Agregar los productos al PDF
        pdf.set_font("Arial", "", 8)
        for producto in productos:
            codBarras, nombre, cantidad, proveedor, especificaciones, fechaCad, costoCompra, costoVenta = producto
            pdf.cell(20, 10, str(codBarras), 1)
            pdf.cell(30, 10, nombre[:20], 1)  # Limita la longitud del nombre a 20 caracteres
            pdf.cell(15, 10, str(cantidad), 1)
            pdf.cell(30, 10, proveedor[:20], 1)
            pdf.cell(30, 10, especificaciones[:20], 1)
            pdf.cell(20, 10, str(fechaCad), 1)
            pdf.cell(20, 10, f"${costoCompra:.2f}", 1)
            pdf.cell(20, 10, f"${costoVenta:.2f}", 1)
            pdf.ln()
        
        # Guardar el PDF
        pdf_file_path = f"ReporteProductos_{numero_consecutivo}_{datetime.now().strftime('%Y%m%d')}.pdf"
        pdf.output(pdf_file_path)
        
        messagebox.showinfo("Reporte generado", f"El reporte se ha guardado como {pdf_file_path}")
        
        # Cerrar la conexión a la base de datos
        cursor.close()
        conexion.close()
        
    except mysql.connector.Error as err:
        messagebox.showerror("Error de base de datos", f"Error: {err}")
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado: {e}")
        
# Función para generar el reporte de productos
def generar_reporte_usuarios():
    try:
        # Conexión a la base de datos
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        # Consulta para obtener los datos de la tabla productos
        cursor.execute("SELECT nombre, ap, am, clave, telefono, correo, contras FROM usuarios")
        usuarios = cursor.fetchall()
        
        if not usuarios:
            messagebox.showinfo("Sin datos", "No hay usuarios registrados para generar el reporte.")
            return
        # Obtener el número consecutivo para el archivo
        numero_consecutivo = obtener_numero_consecutivo()
        # Crear el PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        
        # Título del PDF
        pdf.set_text_color(0, 0, 0)  
        pdf.cell(200, 10, txt="Reporte de Empleados", ln=True, align="C")
        pdf.ln(10)
        
        # Encabezado de la tabla
        pdf.set_fill_color(206, 216, 254) 
        pdf.set_text_color(0, 0, 0)  
        pdf.set_font("Arial", "B", 8)
        pdf.cell(20, 10, "Nombre", 1)
        pdf.cell(25, 10, "Apellido P.", 1)
        pdf.cell(25, 10, "Apellido M.", 1)
        pdf.cell(15, 10, "Clave", 1)
        pdf.cell(20, 10, "Teléfono", 1)
        pdf.cell(40, 10, "Correo", 1)
        pdf.cell(25, 10, "Contraseña", 1)
        pdf.ln()
        
        # Agregar los productos al PDF
        pdf.set_font("Arial", "", 8)
        for usuario in usuarios:
            nombre, ap, am, clave, telefono, correo, contras = usuario
            pdf.cell(20, 10, nombre[:20], 1)
            pdf.cell(25, 10, ap[:20], 1)  # Apellido Paterno, limita a 20 caracteres
            pdf.cell(25, 10, am[:20], 1)  # Apellido Materno, limita a 20 caracteres
            pdf.cell(15, 10, str(clave), 1)  # Convierte la clave a string
            pdf.cell(20, 10, str(telefono), 1)  # Convierte el teléfono a string
            pdf.cell(40, 10, correo[:20], 1)  # Limita el correo a 20 caracteres
            pdf.cell(25, 10, contras[:20], 1)  # Limita la contraseña a 20 caracteres
            pdf.ln()
        
        # Guardar el PDF
        pdf_file_path = f"ReporteUsuarios_{numero_consecutivo}_{datetime.now().strftime('%Y%m%d')}.pdf"
        pdf.output(pdf_file_path)
        
        messagebox.showinfo("Reporte generado", f"El reporte se ha guardado como {pdf_file_path}")
        
        # Cerrar la conexión a la base de datos
        cursor.close()
        conexion.close()
        
    except mysql.connector.Error as err:
        messagebox.showerror("Error de base de datos", f"Error: {err}")
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado: {e}")

# Modificación de la ventana principal de reportes
def abrir_ventana_reportes(root):
    ventana_reportes = tk.Toplevel(root)  # Crear una nueva ventana
    ventana_reportes.title("Reportes")
    ventana_reportes.geometry("200x200")

    # Calcular el tamaño de la pantalla y el tamaño de la ventana
    root.update_idletasks()  # Asegurarse de que las dimensiones estén actualizadas
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()
    ancho_ventana = 200
    alto_ventana = 200

    # Calcular la posición para centrar la ventana
    x_centrado = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y_centrado = (alto_pantalla // 2) - (alto_ventana // 2)
    ventana_reportes.geometry(f"{ancho_ventana}x{alto_ventana}+{x_centrado}+{y_centrado}")

    # Botón para crear el reporte de productos
    reporteProductos = tk.Button(ventana_reportes, text="Crear Reporte Productos", command=generar_reporte_productos)
    reporteProductos.pack(pady=10)

    # Botón para crear otro reporte (como ejemplo)
    reporteUsuarios = tk.Button(ventana_reportes, text="Crear Reporte Usuarios", command=generar_reporte_usuarios)
    reporteUsuarios.pack(pady=10)
    
    # Crear el botón de "reporte de ventas" en esta ventana
    boton_reporteVentas = tk.Button(ventana_reportes, text="Ventas", command=lambda:ventanaReportesVentas(root))
    boton_reporteVentas.pack(pady=10)  # Añadir el botón a la nueva ventana
