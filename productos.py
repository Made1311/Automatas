import tkinter as tk
from tkinter import messagebox, ttk
from conexion import conectar_bd  # Importa la función de conexión

# Función para cargar los productos en la tabla
def cargar_productos(tree):
    # Limpiar la tabla antes de cargar nuevos datos
    for row in tree.get_children():
        tree.delete(row)
        
    # Conectar a la base de datos
    conn = conectar_bd()
    cursor = conn.cursor()
    
    # Consulta para obtener todos los productos
    cursor.execute("SELECT * FROM productos")
    
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

    conn.close()

# Función para agregar un nuevo producto
def agregar_producto(codBarras, nombre, cantidad, proveedores, especificaciones, fechaCad, costoCompra, costoVenta, tree):
    # Validación de campos vacíos
    if not all([codBarras, nombre, cantidad, proveedores, especificaciones, fechaCad, costoCompra, costoVenta]):
        messagebox.showwarning("Advertencia", "Todos los campos deben estar completos.")
        return

    try:
        conn = conectar_bd()
        cursor = conn.cursor()

        # Insertar el nuevo producto, sin necesidad de id_p (AUTO_INCREMENT)
        cursor.execute("INSERT INTO productos (codBarras, nombre, cantidad, proveedores, especificaciones, fechaCad, costoCompra, costoVenta) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                       (codBarras, nombre, cantidad, proveedores, especificaciones, fechaCad, costoCompra, costoVenta))
        conn.commit()
        conn.close()

        # Recargar los productos después de agregar
        cargar_productos(tree)
        
    except ValueError:
        messagebox.showerror("Error", "Uno de los valores ingresados no es válido.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar el producto: {e}")
    finally:
        if conn:
            conn.close()
        
def abrir_ventana_productos(root):
    abrir_ventana_productos = tk.Toplevel(root)
    abrir_ventana_productos.title("Gestión de Productos")
    abrir_ventana_productos.geometry("750x450")
    
    # Crear un marco para la tabla y las barras de desplazamiento
    frame_tabla = tk.Frame(abrir_ventana_productos)
    frame_tabla.pack(fill=tk.BOTH, expand=True, pady=10)

    # Crear la barra de desplazamiento vertical
    scrollbar_vertical = tk.Scrollbar(frame_tabla, orient=tk.VERTICAL)
    scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)

    # Crear la barra de desplazamiento horizontal
    scrollbar_horizontal = tk.Scrollbar(frame_tabla, orient=tk.HORIZONTAL)
    scrollbar_horizontal.pack(side=tk.BOTTOM, fill=tk.X)

    # Crear la tabla con encabezados más anchos
    columnas = ("codBarras", "nombre", "cantidad", "proveedores", "especificaciones", "fechaCad", "costoCompra", "costoVenta")
    tree = ttk.Treeview(frame_tabla, columns=columnas, show='headings', 
                        yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set, height=6)

    # Configurar los encabezados y el ancho de las columnas
    tree.heading("codBarras", text="Cod de Barras")
    tree.heading("nombre", text="Nombre")
    tree.heading("cantidad", text="Cantidad")
    tree.heading("proveedores", text="Proveedor")
    tree.heading("especificaciones", text="Especificaciones")
    tree.heading("fechaCad", text="Fecha de Caducidad")
    tree.heading("costoCompra", text="Costo de compra")
    tree.heading("costoVenta", text="Costo de Venta")

    # Ajustar el ancho de cada columna
    tree.column("codBarras", width=80)
    tree.column("nombre", width=120)
    tree.column("cantidad", width=120)
    tree.column("proveedores", width=100)
    tree.column("especificaciones", width=100)
    tree.column("fechaCad", width=130)
    tree.column("costoCompra", width=130)
    tree.column("costoVenta", width=130)

    tree.pack(fill=tk.BOTH, expand=True)

    # Configurar las barras de desplazamiento
    scrollbar_vertical.config(command=tree.yview)
    scrollbar_horizontal.config(command=tree.xview)

    # Formulario para agregar productos
    frame_formulario = tk.Frame(abrir_ventana_productos)
    frame_formulario.pack(pady=10)

    # Eliminar la entrada para ID, ya que es AUTO_INCREMENT
    tk.Label(frame_formulario, text="Código de barras:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entrada_codigo = tk.Entry(frame_formulario)
    entrada_codigo.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_formulario, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entrada_nombre = tk.Entry(frame_formulario)
    entrada_nombre.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_formulario, text="Cantidad:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
    entrada_cantidad = tk.Entry(frame_formulario)
    entrada_cantidad.grid(row=1, column=3, padx=5, pady=5)

    tk.Label(frame_formulario, text="Proveedores:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entrada_proveedores = tk.Entry(frame_formulario)
    entrada_proveedores.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame_formulario, text="Especificaciones:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
    entrada_especificaciones = tk.Entry(frame_formulario)
    entrada_especificaciones.grid(row=2, column=3, padx=5, pady=5)

    tk.Label(frame_formulario, text="Fecha de caducidad:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    entrada_caducidad = tk.Entry(frame_formulario)
    entrada_caducidad.grid(row=3, column=1, padx=5, pady=5)
    
    tk.Label(frame_formulario, text="Costo de compra:").grid(row=3, column=2, padx=5, pady=5, sticky="e")
    entrada_compra = tk.Entry(frame_formulario)
    entrada_compra.grid(row=3, column=3, padx=5, pady=5)
    
    tk.Label(frame_formulario, text="Costo de Venta:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
    entrada_venta = tk.Entry(frame_formulario)
    entrada_venta.grid(row=4, column=1, padx=5, pady=5)

    # Botón para agregar productos
    boton_agregar = tk.Button(frame_formulario, text="Agregar", command=lambda: agregar_producto(
        entrada_codigo.get(), entrada_nombre.get(), entrada_cantidad.get(), entrada_proveedores.get(), entrada_especificaciones.get(), 
        entrada_caducidad.get(), entrada_compra.get(), entrada_venta.get(), tree))
    boton_agregar.grid(row=6, column=0, pady=10)

    # Botón para eliminar productos
    boton_eliminar = tk.Button(frame_formulario, text="Eliminar", command=lambda: eliminar_producto(tree))
    boton_eliminar.grid(row=6, column=1, pady=10)
    
    # Botón para modificar productos
    boton_modificar = tk.Button(frame_formulario, text="Modificar", 
                            command=lambda: modificar_producto(entrada_codigo.get(), entrada_nombre.get(), entrada_cantidad.get(), entrada_proveedores.get(), entrada_especificaciones.get(), 
        entrada_caducidad.get(), entrada_compra.get(), entrada_venta.get(), tree))
    boton_modificar.grid(row=8, column=0, pady=10)

    # Botón para cancelar (limpiar los campos)
    boton_cancelar = tk.Button(frame_formulario, text="Cancelar", 
                           command=lambda: limpiar_campos(entrada_codigo, entrada_nombre, entrada_cantidad, entrada_proveedores, entrada_especificaciones, 
        entrada_caducidad, entrada_compra, entrada_venta))
    boton_cancelar.grid(row=8, column=1, pady=10)

    # Vincular el evento de selección de un producto en la tabla con la función cargar_datos_seleccionados
    tree.bind("<<TreeviewSelect>>", lambda event: cargar_datos_seleccionados(tree, entrada_codigo, entrada_nombre, entrada_cantidad, entrada_proveedores, entrada_especificaciones, 
        entrada_caducidad, entrada_compra, entrada_venta))

    # Cargar los productos al iniciar la ventana
    cargar_productos(tree)
    
def eliminar_producto(tree):
    selected_item = tree.selection()
    if not selected_item:
        # messagebox.showwarning("Advertencia", "Selecciona un producto para eliminar.")
        return

    producto_id = tree.item(selected_item)['values'][0]  # Obtener el ID del producto
    if producto_id:  # Asegurarse de que el ID del producto existe
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id_p = %s", (producto_id,))
        conn.commit()
        conn.close()
        cargar_productos(tree)  # Recargar los productos después de eliminar
    else:
        # messagebox.showwarning("Advertencia", "No se pudo obtener el ID del producto.")
        return

# Función para limpiar los campos del formulario
def limpiar_campos(entrada_codigo, entrada_nombre, entrada_cantidad, entrada_proveedores, entrada_especificaciones, 
        entrada_caducidad, entrada_compra, entrada_venta):
    entrada_codigo.delete(0, tk.END)
    entrada_nombre.delete(0, tk.END)
    entrada_cantidad.delete(0, tk.END)
    entrada_proveedores.delete(0, tk.END)
    entrada_especificaciones.delete(0, tk.END)
    entrada_caducidad.delete(0, tk.END)
    entrada_compra.delete(0, tk.END)
    entrada_venta.delete(0, tk.END)

# Función para cargar los datos seleccionados en los campos de entrada
def cargar_datos_seleccionados(tree, entrada_codigo, entrada_nombre, entrada_cantidad, entrada_proveedores, entrada_especificaciones, 
        entrada_caducidad, entrada_compra, entrada_venta):
    selected_item = tree.selection()
    if not selected_item:
        # messagebox.showwarning("Advertencia", "Selecciona un producto para modificar.")
        return

    # Obtener los datos del producto seleccionado
    valores_producto = tree.item(selected_item)['values']

    # Rellenar los campos de entrada con los valores del producto seleccionado
    entrada_codigo.delete(0, tk.END)
    entrada_codigo.insert(0, valores_producto[1])
    
    entrada_nombre.delete(0, tk.END)
    entrada_nombre.insert(0, valores_producto[2])
    
    entrada_cantidad.delete(0, tk.END)
    entrada_cantidad.insert(0, valores_producto[3])
    
    entrada_proveedores.delete(0, tk.END)
    entrada_proveedores.insert(0, valores_producto[4])
    
    entrada_especificaciones.delete(0, tk.END)
    entrada_especificaciones.insert(0, valores_producto[5])
    
    entrada_caducidad.delete(0, tk.END)
    entrada_caducidad.insert(0, valores_producto[6])
    
    entrada_compra.delete(0, tk.END)
    entrada_compra.insert(0, valores_producto[7])
    
    entrada_venta.delete(0, tk.END)
    entrada_venta.insert(0, valores_producto[8])

# Función para modificar los datos del producto
def modificar_producto(codBarras, nombre, cantidad, proveedores, especificaciones, fechaCad, costoCompra, costoVenta, tree):
    selected_item = tree.selection()
    if not selected_item:
        # messagebox.showwarning("Advertencia", "Selecciona un producto para modificar.")
        return

    # Obtener el id del producto seleccionado
    id_p = tree.item(selected_item)['values'][0]  # El id está en el primer valor

    conn = conectar_bd()
    cursor = conn.cursor()

    # Consulta para actualizar el producto
    cursor.execute("""
        UPDATE productos 
        SET codBarras = %s, nombre = %s, cantidad = %s, proveedores = %s, especificaciones = %s, fechaCad = %s, costoCompra = %s, costoVenta = %s
        WHERE id_p = %s
    """, (codBarras, nombre, cantidad, proveedores, especificaciones, fechaCad, costoCompra, costoVenta, id_p))
    
    conn.commit()
    conn.close()
    
    cargar_productos(tree)  # Recargar los productos en la tabla después de la modificación