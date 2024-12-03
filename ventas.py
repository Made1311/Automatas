import tkinter as tk
import random
import json
from tkinter import messagebox, ttk
from conexion import conectar_bd  # Importa la función de conexión
import mysql.connector
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from fpdf import FPDF

from reportlab.pdfgen import canvas
import sqlite3 
global nombre_usuario
def obtener_clientes():
    # Conectar a la base de datos
    conexion = conectar_bd()
    cursor = conexion.cursor()
    # Ejecutar la consulta para obtener los clientes
    cursor.execute("SELECT nombre, apellidoP, apellidoM FROM clientes")
    # Obtener todos los resultados
    clientes = cursor.fetchall()
    # Cerrar la conexión
    conexion.close()
    # Formatear los nombres completos de los clientes
    clientes_formateados = [f"{cliente[0]} {cliente[1]} {cliente[2]}" for cliente in clientes]
    return clientes_formateados

# Función para obtener el producto desde la base de datos usando el código de barras
def obtener_producto_por_codigo(codigo_barras):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    # Ejecutar la consulta para obtener el producto por código de barras
    cursor.execute("SELECT nombre, costoVenta FROM productos WHERE codBarras = %s", (codigo_barras,))
    producto = cursor.fetchone()
    conexion.close()
    return producto

# Esta es la ventana principal de "Ventas"
def abrir_ventana_ventas(root, nombre_usuario):
    ventana_ventas = tk.Toplevel(root)  # Crear una nueva ventana
    ventana_ventas.title("Ventas")

    # Agregar botones de opciones de Venta, Devolución y Garantía
    opcion_venta = tk.Button(ventana_ventas, text="Venta", command=lambda: mostrar_venta(ventana_ventas, nombre_usuario))
    opcion_venta.pack(pady=10)
    
    opcion_devolucion = tk.Button(ventana_ventas, text="Devolución")
    opcion_devolucion.pack(pady=10)
    
    opcion_garantia = tk.Button(ventana_ventas, text="Garantía")
    opcion_garantia.pack(pady=10)

# Función para mostrar la sección de "Venta"
def mostrar_venta(ventana,nombre_usuario):

    # Limpiar la ventana si ya hay algo cargado
    for widget in ventana.winfo_children():
        widget.destroy()

    # Mostrar el nombre del usuario
    label_usuario = tk.Label(ventana, text=f"Usuario: {nombre_usuario}")  # Cargar el nombre del usuario dinámicamente
    label_usuario.pack(pady=10)
    global tabla_productos, label_total, combo_cliente
    
    def agregar_producto():
        codigo_barras = entry_cod_barras.get()
        if not codigo_barras:
            messagebox.showerror("Error", "Debe ingresar un código de barras.")
            return
        producto = obtener_producto_por_codigo(codigo_barras)
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado.")
            return
        nombre_producto, costo_producto = producto
        cantidad = 1
        subtotal = cantidad * costo_producto
        tabla_productos.insert("", "end", values=(codigo_barras, nombre_producto, costo_producto, cantidad, subtotal))
        actualizar_total()

    def actualizar_total():
        total = sum(float(tabla_productos.item(item, "values")[4]) for item in tabla_productos.get_children())
        label_total.config(text=f"Total: ${total:.2f}")
        
    # Crear campo de búsqueda de productos por código de barras
    label_cod_barras = tk.Label(ventana, text="Código de Barras:")
    label_cod_barras.pack(pady=5)
           # Botón para agregar productos
    boton_agregar_producto = tk.Button(ventana, text="Agregar Producto", command=agregar_producto)
    boton_agregar_producto.pack(pady=10)
    
    entry_cod_barras = tk.Entry(ventana)
    entry_cod_barras.pack(pady=5)

   # Crear un ComboBox para seleccionar el cliente
    label_cliente = tk.Label(ventana, text="Cliente:")
    label_cliente.pack(pady=5)
    
    # Obtener los clientes de la base de datos
    clientes = obtener_clientes()

    # Crear el ComboBox y cargar los clientes
    combo_cliente = ttk.Combobox(ventana)
    combo_cliente['values'] = clientes  # Asignar los nombres completos de los clientes
    combo_cliente.pack(pady=5)

    # Crear un botón para agregar un nuevo cliente
    def agregar_cliente():
        # Aquí se pueden agregar los datos del cliente con un formulario
        pass
    
    boton_agregar_cliente = tk.Button(ventana, text="Agregar Cliente", command=agregar_cliente)
    boton_agregar_cliente.pack(pady=10)

   # Crear tabla para productos seleccionados (Código, Nombre, Costo, Cantidad, Subtotal)
    columnas = ('Código', 'Nombre', 'Costo', 'Cantidad', 'Subtotal')
    tabla_productos = ttk.Treeview(ventana, columns=columnas, show='headings')
    for col in columnas:
        tabla_productos.heading(col, text=col)
    tabla_productos.pack(pady=10)
    # Mostrar el total
    label_total = tk.Label(ventana, text="Total: $0.00")
    label_total.pack(pady=5)
    
        
        # Doble clic en una fila para editar la cantidad
    def editar_cantidad(event):
        selected_item = tabla_productos.selection()
        if not selected_item:
            return
        item = selected_item[0]
        values = tabla_productos.item(item, "values")
        codigo_barras, nombre_producto, costo_producto, cantidad_actual, subtotal = values

        # Crear una ventana emergente para cambiar la cantidad
        top = tk.Toplevel(ventana)
        top.title("Editar Cantidad")
        top.geometry("250x150")

        label = tk.Label(top, text="Cantidad:")
        label.pack(pady=10)
        
        # Spinbox para cambiar la cantidad
        spinbox_cantidad = tk.Spinbox(top, from_=1, to=100, width=5)
        spinbox_cantidad.pack(pady=5)
        spinbox_cantidad.delete(0, "end")
        spinbox_cantidad.insert(0, cantidad_actual)

        def actualizar_cantidad():
            nueva_cantidad = int(spinbox_cantidad.get())
            nuevo_subtotal = nueva_cantidad * float(costo_producto)
            tabla_productos.item(item, values=(codigo_barras, nombre_producto, costo_producto, nueva_cantidad, nuevo_subtotal))
            top.destroy()
            actualizar_total() 

        boton_actualizar = tk.Button(top, text="Actualizar", command=actualizar_cantidad)
        boton_actualizar.pack(pady=10)

    # Asociar el evento de doble clic para editar la cantidad
    tabla_productos.bind("<Double-1>", editar_cantidad)

    def obtener_productos_seleccionados():
        productos = []
        for item in tabla_productos.get_children():
            producto = tabla_productos.item(item, "values")
            productos.append(producto)  # Agregar tu formato de producto aquí (ej. código, nombre, costo, cantidad, subtotal)
        return productos
    def cantidad_productos():
        return len(tabla_productos.get_children())  # Retorna la cantidad de productos en la tabla

    # Funciones para eliminar productos
    def eliminar_ultimo_producto():
        tabla_productos.delete(tabla_productos.get_children()[-1])
        actualizar_total()

    def eliminar_todos_los_productos():
        for item in tabla_productos.get_children():
            tabla_productos.delete(item)
        actualizar_total()
        
    boton_eliminar_ultimo = tk.Button(ventana, text="Eliminar Último Producto", command=eliminar_ultimo_producto)
    boton_eliminar_ultimo.pack(pady=5)

    boton_eliminar_todos = tk.Button(ventana, text="Eliminar Todos los Productos", command=eliminar_todos_los_productos)
    boton_eliminar_todos.pack(pady=5)
    
    
    
    tk.Button(ventana, text="Pagar con Efectivo",  command=lambda: pago_efectivo(ventana, nombre_usuario)).pack(pady=10)
    tk.Button(ventana, text="Tarjeta", command=lambda: pago_tarjeta(ventana, nombre_usuario, combo_cliente.get(), obtener_productos_seleccionados(), cantidad_productos())).pack(pady=5)

# Función para generar PDF de la venta
def generar_pdf_venta(cliente, nombre_usuario, productos, total, efectivo, cambio, tipo_pago):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    
    # Título del PDF
    pdf.cell(200, 10, txt="Ticket de Venta", ln=True, align="C")
    pdf.ln(10)
    
    # Detalles de la venta
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=True)
    pdf.cell(200, 10, txt=f"Atendido por: {nombre_usuario}", ln=True)
    pdf.cell(200, 10, txt=f"Tipo de Pago: {tipo_pago}", ln=True)
    pdf.cell(200, 10, txt=f"Total: ${total:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Efectivo: ${efectivo:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Cambio: ${cambio:.2f}", ln=True)
    pdf.ln(10)

    # Encabezado de la tabla de productos
    pdf.cell(40, 10, "Código", 1)
    pdf.cell(70, 10, "Producto", 1)
    pdf.cell(30, 10, "Costo", 1)
    pdf.cell(20, 10, "Cantidad", 1)
    pdf.cell(30, 10, "Subtotal", 1)
    pdf.ln()

    # Detalles de los productos
    for item in productos:
        codigo, nombre, costo, cantidad, subtotal = item
        pdf.cell(40, 10, str(codigo), 1)
        pdf.cell(70, 10, nombre, 1)
        pdf.cell(30, 10, f"${costo}", 1)
        pdf.cell(20, 10, str(cantidad), 1)
        pdf.cell(30, 10, f"${subtotal}", 1)
        pdf.ln()

    # Guardar el PDF
    pdf_file_path = f"venta_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(pdf_file_path)
    messagebox.showinfo("PDF generado", f"El PDF se ha guardado como {pdf_file_path}")

# Función para simular la verificación de conexión
def verificar_conexion():
    # Simulación aleatoria de conexión (50% de probabilidad de tener internet)
    return random.choice([True, False])

def generar_ticket(nombre_usuario, total, banco_seleccionado, pin):
    # Simular la generación de un ticket de compra
    ticket = f"--- TICKET ---\nUsuario: {nombre_usuario}\nTotal: ${total:.2f}\nBanco: {banco_seleccionado}\nPIN: {pin}\n--- Gracias por su compra! ---"
    return ticket

def guardar_venta_en_bd(nombre_usuario, cliente, productos, cantidadP, total, banco_seleccionado, tipo_pago):
    # Conexión a la base de datos (utilizando la función de conexión)
    conn = conectar_bd()
    cursor = conn.cursor()

    # Serializar la lista de productos a JSON
    productos_json = json.dumps(productos)  # Convertir la lista de productos a una cadena JSON

    # Si el pago es con tarjeta, asignamos 0 a 'efectivo' y 'cambio'
    if tipo_pago == "Tarjeta":
        efectivo = 0
        cambio = 0
    else:
        efectivo = 0  # Asegúrate de ajustar este valor según sea necesario
        cambio = 0     # Asegúrate de ajustar este valor según sea necesario

    # Obtener la fecha y hora actual
    fecha_actual = datetime.now()

    # Insertar los datos de la venta
    cursor.execute("""
        INSERT INTO ventas (nombreU, cliente, productos, cantidadP, efectivo, cambio, total, tipoPago, fecha)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (nombre_usuario, cliente, productos_json, cantidadP, efectivo, cambio, total, tipo_pago, fecha_actual))

    # Confirmar y cerrar la conexión
    conn.commit()
    conn.close()
    
def obtener_venta_por_id(venta_id):
    # Conexión a la base de datos
    conn = conectar_bd()
    cursor = conn.cursor()

    # Obtener la venta
    cursor.execute("SELECT * FROM ventas WHERE id_venta = %s", (venta_id,))
    venta = cursor.fetchone()

    if venta:
        # Deserializar la cadena JSON de productos
        productos_json = venta[2]  # Suponiendo que 'productos' está en la columna 3
        productos = json.loads(productos_json)  # Convertir la cadena JSON de vuelta a una lista

    conn.close()
    return venta

def pago_tarjeta(ventana, nombre_usuario, cliente, productos, cantidadP):
    print(f"Cliente: {cliente}, Productos: {productos}, Cantidad: {cantidadP}")
    total_actual = float(label_total.cget("text").split(": $")[1])

    # Crear la ventana emergente para el pago con tarjeta
    top = tk.Toplevel(ventana)
    top.title("Pago con Tarjeta")
    top.geometry("400x300")

    # Verificar si hay conexión a internet
    conexion_activa = verificar_conexion()

    # Mostrar el estado de la conexión
    if conexion_activa:
        estado_red = "Red: Conectado"
        label_banco = tk.Label(top, text="Banco:")
        label_banco.pack(pady=5)

        # Crear el ComboBox para seleccionar el banco
        bancos = [("BBVA", "1100", 0), ("Banorte", "1110", 0.08), 
                  ("Banco Azteca", "1111", 0.10), ("Santander", "1112", 0.10), 
                  ("American Express", "1123", 0.12)]
        
        combo_banco = ttk.Combobox(top, values=[f"{banco[0]} ({banco[1]})" for banco in bancos])
        combo_banco.pack(pady=5)

        # Crear el campo para el número de tarjeta
        label_numero_tarjeta = tk.Label(top, text="Código de Tarjeta:")
        label_numero_tarjeta.pack(pady=5)
        entry_numero_tarjeta = tk.Entry(top)
        entry_numero_tarjeta.pack(pady=5)
        entry_numero_tarjeta.insert(0, "----")

        # Función para calcular el total con interés
        def calcular_total_con_interes():
            banco_seleccionado = combo_banco.get()
            if banco_seleccionado:
                # Obtener el porcentaje de interés según el banco seleccionado
                banco = next((banco for banco in bancos if banco_seleccionado.startswith(banco[0])), None)
                if banco:
                    interes = banco[2]
                    total_con_interes = total_actual * (1 + interes)
                    label_total_interes.config(text=f"Total con interés: ${total_con_interes:.2f}")
                else:
                    messagebox.showerror("Error", "Banco no válido")
            else:
                messagebox.showerror("Error", "Debe seleccionar un banco")

        # Botón para calcular el total con interés
        boton_calcular = tk.Button(top, text="Calcular Total con Interés", command=calcular_total_con_interes)
        boton_calcular.pack(pady=10)

        # Mostrar el total con interés
        label_total_interes = tk.Label(top, text="Total con interés: $0.00")
        label_total_interes.pack(pady=5)

        # Función para confirmar el pago
        def confirmar_pago():
            banco_seleccionado = combo_banco.get()
            if banco_seleccionado:
                # Solicitar PIN
                def ingresar_pin():
                    pin = entry_pin.get()
                    if len(pin) == 4 and pin.isdigit():  # Validación de PIN (4 dígitos)
                        # Guardar la venta en la base de datos
                        total_con_interes = float(label_total_interes.cget("text").split(": $")[1])
                        tipo_pago = "Tarjeta"
                        guardar_venta_en_bd(nombre_usuario, cliente, productos, cantidadP, total_con_interes, banco_seleccionado, tipo_pago)
                        
                        # Generar y mostrar el ticket
                        ticket = generar_ticket(nombre_usuario, total_con_interes, banco_seleccionado, pin)
                        messagebox.showinfo("Pago Exitoso", f"Pago realizado exitosamente. {ticket}")
                        top.destroy()
                    else:
                        messagebox.showerror("Error", "El PIN debe tener 4 dígitos numéricos")

                # Crear ventana para ingresar el PIN
                pin_window = tk.Toplevel(top)
                pin_window.title("Ingrese el PIN")
                pin_window.geometry("300x200")

                label_pin = tk.Label(pin_window, text="Ingrese su PIN (4 dígitos):")
                label_pin.pack(pady=10)
                entry_pin = tk.Entry(pin_window, show="*")
                entry_pin.pack(pady=10)

                boton_confirmar_pin = tk.Button(pin_window, text="Confirmar", command=ingresar_pin)
                boton_confirmar_pin.pack(pady=10)

            else:
                messagebox.showerror("Error", "Debe seleccionar un banco")

        # Función para cancelar el pago
        def cancelar_pago():
            top.destroy()

        # Botones de Confirmar y Cancelar
        boton_confirmar = tk.Button(top, text="Confirmar", command=confirmar_pago)
        boton_confirmar.pack(side=tk.LEFT, padx=10, pady=20)

        boton_cancelar = tk.Button(top, text="Cancelar", command=cancelar_pago)
        boton_cancelar.pack(side=tk.RIGHT, padx=10, pady=20)

    else:
        messagebox.showerror("Error", "No hay conexión a Internet. Intente más tarde.")

# Botón para pago con tarjeta que abre la ventana de `pago_tarjeta`
   # tk.Button(ventana, text="Tarjeta", command=lambda: pago_tarjeta(top, nombre_usuario)).pack(pady=5)
   # tk.Button.pack(pady=10)

# Función de pago con efectivo
def pago_efectivo(ventana, nombre_usuario):
    total_actual = float(label_total.cget("text").split(": $")[1])

    top = tk.Toplevel(ventana)
    top.title("Pago con Efectivo")
    top.geometry("300x200")

    label_total_pago = tk.Label(top, text=f"Total a Pagar: ${total_actual:.2f}")
    label_total_pago.pack(pady=10)

    label_efectivo = tk.Label(top, text="Monto en Efectivo:")
    label_efectivo.pack(pady=5)

    campo_efectivo = tk.Entry(top)
    campo_efectivo.pack(pady=5)

    label_cambio = tk.Label(top, text="Cambio: $0.00")
    label_cambio.pack(pady=10)

    def calcular_cambio():
        try:
            efectivo = float(campo_efectivo.get())
            if efectivo < total_actual:
                messagebox.showerror("Error", "El monto de efectivo es menor al total.")
                return
            cambio = efectivo - total_actual
            label_cambio.config(text=f"Cambio: ${cambio:.2f}")
            return cambio, efectivo
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un monto válido.")
            return None, None

    def generar_ticket(nombre_usuario):
        cambio, efectivo = calcular_cambio()
        if cambio is None:
            return

        fecha = datetime.now().strftime('%Y-%m-%d')
        cliente = combo_cliente.get()
        nombreU = nombre_usuario
        productos = [(tabla_productos.item(item, "values")[0], 
                      tabla_productos.item(item, "values")[1],
                      float(tabla_productos.item(item, "values")[2]),
                      int(tabla_productos.item(item, "values")[3]),
                      float(tabla_productos.item(item, "values")[4])) 
                     for item in tabla_productos.get_children()]
        cantidadP = sum(int(tabla_productos.item(item, "values")[3]) for item in tabla_productos.get_children())
        tipoPago = "Efectivo"

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO ventas (fecha, nombreU, cliente, productos, cantidadP, total, efectivo, cambio, tipoPago)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (fecha, nombreU, cliente, ", ".join([p[1] for p in productos]), cantidadP, total_actual, efectivo, cambio, tipoPago))

            conexion.commit()
            messagebox.showinfo("Éxito", "Venta registrada exitosamente.")
            
            # Generar el PDF después de guardar en la base de datos
            generar_pdf_venta(cliente, nombreU, productos, total_actual, efectivo, cambio, tipoPago)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo guardar la venta: {err}")
        finally:
            conexion.close()
            top.destroy()

    tk.Button(top, text="Calcular Cambio", command=calcular_cambio).pack(pady=5)
    boton_generar_ticket = tk.Button(top, text="Generar Ticket", command=lambda: generar_ticket(nombre_usuario))
    boton_generar_ticket.pack(pady=20)
# Función para obtener las ventas de la base de datos filtradas por periodo
def obtener_ventas(periodo, usuario=None):
    conexion = conectar_bd()
    cursor = conexion.cursor()

    # Calcular las fechas para el filtro
    if periodo == "día":
        fecha_inicio = datetime.now().date()
        fecha_fin = fecha_inicio
    elif periodo == "semana":
        fecha_inicio = (datetime.now() - timedelta(days=datetime.now().weekday())).date()
        fecha_fin = fecha_inicio + timedelta(days=6)
    elif periodo == "mes":
        fecha_inicio = datetime.now().replace(day=1).date()
        fecha_fin = (fecha_inicio + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    else:
        fecha_inicio, fecha_fin = None, None

    # Construir consulta SQL
    query = f"""
        SELECT id_venta, fecha, nombreU, cliente, productos, cantidadP, total, tipoPago 
        FROM ventas
        WHERE fecha BETWEEN %s AND %s
    """
    params = [fecha_inicio, fecha_fin]

    if usuario:
        query += " AND nombreU = %s"
        params.append(usuario)

    cursor.execute(query, params)
    ventas = cursor.fetchall()
    conexion.close()
    return ventas

# Función para generar un reporte PDF
def generar_reporte_pdf(periodo, ventas):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)

    # Título del reporte
    pdf.cell(200, 10, txt=f"Reporte de Ventas por {periodo.capitalize()}", ln=True, align="C")
    pdf.ln(10)

    # Encabezados de la tabla
    pdf.set_font("Arial", "B", 12)
    pdf.cell(20, 10, "ID", 1)
    pdf.cell(30, 10, "Fecha", 1)
    pdf.cell(30, 10, "Usuario", 1)
    pdf.cell(30, 10, "Cliente", 1)
    pdf.cell(40, 10, "Productos", 1)
    pdf.cell(20, 10, "Cantidad", 1)
    pdf.cell(20, 10, "Total", 1)
    pdf.cell(30, 10, "Pago", 1)
    pdf.ln()

    # Contenido de la tabla
    pdf.set_font("Arial", "", 10)
    for venta in ventas:
        pdf.cell(20, 10, str(venta[0]), 1)
        pdf.cell(30, 10, str(venta[1]), 1)
        pdf.cell(30, 10, venta[2], 1)
        pdf.cell(30, 10, venta[3], 1)
        pdf.cell(40, 10, venta[4], 1)
        pdf.cell(20, 10, str(venta[5]), 1)
        pdf.cell(20, 10, f"${venta[6]:.2f}", 1)
        pdf.cell(30, 10, venta[7], 1)
        pdf.ln()

    # Guardar el PDF
    pdf_file_path = f"reporte_ventas_{periodo}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(pdf_file_path)
    messagebox.showinfo("PDF generado", f"El reporte se ha guardado como {pdf_file_path}")
    
def obtener_usuarios():
    # Conectar a la base de datos
    conexion = conectar_bd()
    cursor = conexion.cursor()

    # Consulta para obtener los nombres de usuario
    cursor.execute("SELECT DISTINCT nombreU FROM ventas")
    usuarios = cursor.fetchall()

    # Cerrar la conexión
    conexion.close()

    # Formatear la lista de usuarios
    usuarios_lista = [usuario[0] for usuario in usuarios]
    return usuarios_lista
