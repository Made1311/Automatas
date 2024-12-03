import tkinter as tk
from tkinter import messagebox, ttk
from conexion import conectar_bd  # Importa la función de conexión

# Función para cargar los usuarios en la tabla
def cargar_usuarios(tree):
    # Limpiar la tabla antes de cargar nuevos datos
    for row in tree.get_children():
        tree.delete(row)
        
    # Conectar a la base de datos
    conn = conectar_bd()
    cursor = conn.cursor()
    
    # Consulta para obtener todos los usuarios
    cursor.execute("SELECT * FROM usuarios")
    
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

    conn.close()
# Función para agregar un nuevo usuario
def agregar_usuario(nombre, ap, am, clave, telefono, correo, contras, tree):
    # Validación de campos vacíos
    if not all([nombre, ap, am, clave, telefono, correo, contras]):
        messagebox.showwarning("Advertencia", "Todos los campos deben estar completos.")
        return

    try:
        conn = conectar_bd()
        cursor = conn.cursor()

        # Insertar el nuevo usuario, no necesitamos id_u porque es autoincrement
        cursor.execute("INSERT INTO usuarios (nombre, ap, am, clave, telefono, correo, contras) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                       (nombre, ap, am, clave, telefono, correo, contras))
        conn.commit()
        conn.close()

        # Recargar los usuarios después de agregar
        cargar_usuarios(tree)
        # messagebox.showinfo("Éxito", "Usuario agregado correctamente.")
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar el usuario: {e}")
    finally:
        conn.close()
        
# Función para abrir la ventana de gestión de usuarios
def abrir_ventana_usuarios(root):
    ventana_usuarios = tk.Toplevel(root)
    ventana_usuarios.title("Gestión de Usuarios")
    ventana_usuarios.geometry("750x500")

    # Crear un marco para la tabla y las barras de desplazamiento
    frame_tabla = tk.Frame(ventana_usuarios)
    frame_tabla.pack(fill=tk.BOTH, expand=True, pady=10)

    # Crear la barra de desplazamiento vertical
    scrollbar_vertical = tk.Scrollbar(frame_tabla, orient=tk.VERTICAL)
    scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)

    # Crear la barra de desplazamiento horizontal
    scrollbar_horizontal = tk.Scrollbar(frame_tabla, orient=tk.HORIZONTAL)
    scrollbar_horizontal.pack(side=tk.BOTTOM, fill=tk.X)

    # Crear la tabla con encabezados más anchos
    columnas = ("id_u", "nombre", "ap", "am", "clave", "telefono", "correo")
    tree = ttk.Treeview(frame_tabla, columns=columnas, show='headings', 
                        yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set, height=6)

    # Configurar los encabezados y el ancho de las columnas
    tree.heading("id_u", text="ID")
    tree.heading("nombre", text="Nombre")
    tree.heading("ap", text="Apellido Paterno")
    tree.heading("am", text="Apellido Materno")
    tree.heading("clave", text="Clave")
    tree.heading("telefono", text="Teléfono")
    tree.heading("correo", text="Correo")

    # Ajustar el ancho de cada columna
    tree.column("id_u", width=30)
    tree.column("nombre", width=80)
    tree.column("ap", width=120)
    tree.column("am", width=120)
    tree.column("clave", width=100)
    tree.column("telefono", width=100)
    tree.column("correo", width=130)

    tree.pack(fill=tk.BOTH, expand=True)

    # Configurar las barras de desplazamiento
    scrollbar_vertical.config(command=tree.yview)
    scrollbar_horizontal.config(command=tree.xview)

    # Formulario para agregar usuarios
    frame_formulario = tk.Frame(ventana_usuarios)
    frame_formulario.pack(pady=10)

    # Formulario para agregar usuarios
    tk.Label(frame_formulario, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entrada_nombre = tk.Entry(frame_formulario)
    entrada_nombre.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_formulario, text="Apellido Paterno:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    entrada_ap = tk.Entry(frame_formulario)
    entrada_ap.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(frame_formulario, text="Apellido Materno:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entrada_am = tk.Entry(frame_formulario)
    entrada_am.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_formulario, text="Clave:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
    entrada_clave = tk.Entry(frame_formulario)
    entrada_clave.grid(row=1, column=3, padx=5, pady=5)

    tk.Label(frame_formulario, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entrada_telefono = tk.Entry(frame_formulario)
    entrada_telefono.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame_formulario, text="Correo:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
    entrada_correo = tk.Entry(frame_formulario)
    entrada_correo.grid(row=2, column=3, padx=5, pady=5)

    tk.Label(frame_formulario, text="Contraseña:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    entrada_contra = tk.Entry(frame_formulario, show="*")  # Contraseña oculta
    entrada_contra.grid(row=3, column=1, padx=5, pady=5)

    # Botón para agregar usuarios
    boton_agregar = tk.Button(frame_formulario, text="Agregar", command=lambda: agregar_usuario(
        entrada_nombre.get(), entrada_ap.get(), entrada_am.get(), entrada_clave.get(), 
        entrada_telefono.get(), entrada_correo.get(), entrada_contra.get(), tree))
    boton_agregar.grid(row=7, column=0, pady=10)

    # Botón para eliminar usuarios
    boton_eliminar = tk.Button(frame_formulario, text="Eliminar", command=lambda: eliminar_usuario(tree))
    boton_eliminar.grid(row=7, column=1, pady=10)
    
    # Botón para modificar usuarios
    boton_modificar = tk.Button(frame_formulario, text="Modificar", 
                            command=lambda: modificar_usuario(entrada_nombre.get(), entrada_ap.get(), entrada_am.get(), entrada_clave.get(), 
                                                              entrada_telefono.get(), entrada_correo.get(), entrada_contra.get(), tree))
    boton_modificar.grid(row=8, column=0, pady=10)

    # Botón para cancelar (limpiar los campos)
    boton_cancelar = tk.Button(frame_formulario, text="Cancelar", 
                           command=lambda: limpiar_campos(entrada_nombre, entrada_ap, entrada_am, entrada_clave, entrada_telefono, entrada_correo, entrada_contra))
    boton_cancelar.grid(row=8, column=1, pady=10)

    # Vincular el evento de selección de un usuario en la tabla con la función cargar_datos_seleccionados
    tree.bind("<<TreeviewSelect>>", lambda event: cargar_datos_seleccionados(tree, entrada_nombre, entrada_ap, entrada_am, entrada_clave, entrada_telefono, entrada_correo, entrada_contra))

    # Cargar los usuarios al iniciar la ventana
    cargar_usuarios(tree)
    
def eliminar_usuario(tree):
    selected_item = tree.selection()
    if not selected_item:
     #   messagebox.showwarning("Advertencia", "Selecciona un usuario para eliminar.")
        return

    usuario_id = tree.item(selected_item)['values'][0]  # Obtener el ID del usuario
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id_u = %s", (usuario_id,))
    conn.commit()
    conn.close()
    cargar_usuarios(tree)

# Función para limpiar los campos del formulario
def limpiar_campos(entrada_nombre, entrada_ap, entrada_am, entrada_clave, entrada_telefono, entrada_correo, entrada_contra):
    entrada_nombre.delete(0, tk.END)
    entrada_ap.delete(0, tk.END)
    entrada_am.delete(0, tk.END)
    entrada_clave.delete(0, tk.END)
    entrada_telefono.delete(0, tk.END)
    entrada_correo.delete(0, tk.END)
    entrada_contra.delete(0, tk.END)  # Limpiar el campo de la contraseña

# Función para cargar los datos seleccionados en los campos de entrada
def cargar_datos_seleccionados(tree, entrada_nombre, entrada_ap, entrada_am, entrada_clave, entrada_telefono, entrada_correo, entrada_contra):
    selected_item = tree.selection()
    if not selected_item:
        # messagebox.showwarning("Advertencia", "Selecciona un usuario para modificar.")
        return

    # Obtener los datos del usuario seleccionado
    valores_usuario = tree.item(selected_item)['values']

    # Rellenar los campos de entrada con los valores del usuario seleccionado
    entrada_nombre.delete(0, tk.END)
    entrada_nombre.insert(0, valores_usuario[1])
    
    entrada_ap.delete(0, tk.END)
    entrada_ap.insert(0, valores_usuario[2])
    
    entrada_am.delete(0, tk.END)
    entrada_am.insert(0, valores_usuario[3])
    
    entrada_clave.delete(0, tk.END)
    entrada_clave.insert(0, valores_usuario[4])
    
    entrada_telefono.delete(0, tk.END)
    entrada_telefono.insert(0, valores_usuario[5])
    
    entrada_correo.delete(0, tk.END)
    entrada_correo.insert(0, valores_usuario[6])

    # Cargar la contraseña en el campo correspondiente
    entrada_contra.delete(0, tk.END)
    entrada_contra.insert(0, valores_usuario[7])  # Suponiendo que el campo de contraseña es el último en los valores

# Función para modificar los datos del usuario
def modificar_usuario(nombre, ap, am, clave, telefono, correo, contra, tree):
    selected_item = tree.selection()
    if not selected_item:
        # messagebox.showwarning("Advertencia", "Selecciona un usuario para modificar.")
        return
    # Obtener el ID del usuario seleccionado
    usuario_id = tree.item(selected_item)['values'][0]  # El ID está en la primera columna
    conn = conectar_bd()
    cursor = conn.cursor()
    # Consulta para actualizar el usuario
    cursor.execute("""
        UPDATE usuarios 
        SET nombre = %s, ap = %s, am = %s, clave = %s, telefono = %s, correo = %s, contra = %s
        WHERE id_u = %s
    """, (nombre, ap, am, clave, telefono, correo, contra, usuario_id))
    conn.commit()
    conn.close()
    cargar_usuarios(tree)  # Recargar los usuarios en la tabla después de la modificación