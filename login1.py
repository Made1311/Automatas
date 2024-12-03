import re
import tkinter as tk
from tkinter import messagebox
from usuarios import abrir_ventana_usuarios  # Importa la función de usuarios.py
from productos import abrir_ventana_productos  # Importa la función de productos.py
from ventas import abrir_ventana_ventas
from reportes import abrir_ventana_reportes;
from conexion import conectar_bd
from PIL import Image, ImageTk  # Para manejar imágenes
import random

# Función para verificar usuario y contraseña
def verificar_usuario_contraseña(usuario, contraseña):
    conn = conectar_bd()  # Usamos la función de conexión de tu archivo 'conexion.py'
    cursor = conn.cursor()
    # Consulta para verificar el usuario y la contraseña en la base de datos
    cursor.execute("SELECT * FROM usuarios WHERE nombre = %s AND contras = %s", (usuario, contraseña))
    usuario_encontrado = cursor.fetchone()
    conn.close()  # Cerramos la conexión
    # Si se encuentra el usuario, retorna True, de lo contrario, False
    return usuario_encontrado is not None

# Lista de CAPTCHAs con su respectivo texto
captchas = [
    {"imagen": "captcha1.png", "texto": "QFE534"},
    {"imagen": "captcha2.png", "texto": "Syk84"},
    {"imagen": "captcha3.png", "texto": "TJu483"}
]

# Contador de intentos fallidos
intentos_fallidos = 0

# Función para validar la contraseña en tiempo real
def validar_contraseña(event=None):
    contraseña = entrada_contra.get()
    errores = []

    # Verifica que la contraseña tenga al menos 8 caracteres
    if len(contraseña) < 8:
        errores.append("Debe tener al menos 8 caracteres.")
    
    # Verifica que la contraseña tenga al menos un número
    if not re.search(r'\d', contraseña):
        errores.append("Debe contener al menos un número.")
    
    # Verifica que la contraseña tenga al menos una letra minúscula
    if not re.search(r'[a-z]', contraseña):
        errores.append("Debe contener al menos una letra minúscula.")
    
    # Verifica que la contraseña tenga al menos una letra mayúscula
    if not re.search(r'[A-Z]', contraseña):
        errores.append("Debe contener al menos una letra mayúscula.")
    
    # Verifica que la contraseña tenga al menos un carácter especial
    if not re.search(r'[!@#$%^&*]', contraseña):
        errores.append("Debe contener al menos un carácter especial.")

    # Muestra los errores o limpia el mensaje
    if errores:
        eti_errores.config(text="\n".join(errores), fg="red")
        btn_login.config(state="disabled")
    else:
        eti_errores.config(text="Contraseña válida", fg="green")
        mostrar_captcha()  # Muestra el CAPTCHA cuando la contraseña es válida
        btn_login.config(state="normal")  # Habilita el botón de login

# Función para mostrar un CAPTCHA aleatorio
def mostrar_captcha():
    global captcha_actual
    captcha_actual = random.choice(captchas)
    
    # Cargar la imagen del CAPTCHA
    imagen = Image.open(captcha_actual["imagen"])
    imagen = imagen.resize((150, 50))  # Ajusta el tamaño de la imagen si es necesario
    imagen_tk = ImageTk.PhotoImage(imagen)

    # Mostrar la imagen en la etiquetal
    eti_captcha.config(image=imagen_tk)
    eti_captcha.image = imagen_tk

    # Hacer visible la entrada para el CAPTCHA
    entrada_captcha.pack(pady=5)
    eti_captcha.pack(pady=5)
# Variable global para almacenar el nombre del usuario
nombre_usuario = ""
# Función para obtener el nombre del usuario desde la base de datos
def obtener_nombre_usuario(usuario):
    conn = conectar_bd()  # Usamos la función de conexión de tu archivo 'conexion.py'
    cursor = conn.cursor()
    # Consulta para obtener el nombre del usuario
    cursor.execute("SELECT nombre FROM usuarios WHERE nombre = %s", (usuario,))
    usuario_encontrado = cursor.fetchone()
    conn.close()  # Cerramos la conexión

    if usuario_encontrado:
        return usuario_encontrado[0]  # Retorna el nombre completo del usuario
    else:
        return None  # Si no se encuentra el usuario, retorna None
    
# Función que se ejecuta al presionar el botón de Iniciar Sesión
def login():
    global intentos_fallidos, nombre_usuario  # Aseguramos que 'nombre_usuario' es global
    usuario = entrada_usuario.get()
    contraseña = entrada_contra.get()
    captcha_texto = entrada_captcha.get()

    # Verifica que la contraseña sea válida antes de proceder
    if not eti_errores.cget("text").startswith("Debe"):
        # Verifica si el usuario y la contraseña son correctos
        if verificar_usuario_contraseña(usuario, contraseña):
            # Verifica si el CAPTCHA es correcto
            if captcha_texto == captcha_actual["texto"]:
                # Obtener el nombre del usuario
                nombre_usuario = obtener_nombre_usuario(usuario)  # Almacenar el nombre del usuario
                if nombre_usuario:  # Si el nombre del usuario es válido
                     abrir_nueva_ventana(nombre_usuario)   # Pasamos nombre_usuario como argumento
                else:
                    messagebox.showerror("Error", "Usuario no encontrado.")
            else:
                intentos_fallidos += 1
                messagebox.showerror("Error", f"CAPTCHA incorrecto. Intentos fallidos: {intentos_fallidos}")
        else:
            intentos_fallidos += 1
            messagebox.showerror("Error", f"Nombre de usuario o contraseña incorrectos. Intentos fallidos: {intentos_fallidos}")
    else:
        intentos_fallidos += 1
        messagebox.showerror("Error", f"Contraseña inválida. Intentos fallidos: {intentos_fallidos}")

    # Si hay 3 intentos fallidos, cierra el programa
    if intentos_fallidos >= 3:
        messagebox.showerror("Error", "Demasiados intentos fallidos. El programa se cerrará.")
        root.quit()

# Crear la ventana principal
root = tk.Tk()
root.title("Login")

# Establecer el tamaño de la ventana
root.geometry("400x400")

# Obtener las dimensiones de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Obtener las dimensiones de la ventana
window_width = 400
window_height = 400

# Calcular la posición para centrar la ventana
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Establecer la geometría de la ventana con la posición calculada
root.geometry(f'{window_width}x{window_height}+{x}+{y}')

# Etiqueta y campo para el nombre de usuario
eti_usuario = tk.Label(root, text="Usuario:")
eti_usuario.pack(pady=5)
entrada_usuario = tk.Entry(root, width=30)
entrada_usuario.pack(pady=5)

# Etiqueta y campo para la contraseña
eti_contra = tk.Label(root, text="Contraseña:")
eti_contra.pack()
entrada_contra = tk.Entry(root, show="*", width=30)
entrada_contra.pack()
entrada_contra.bind("<KeyRelease>", validar_contraseña)  # Valida en tiempo real al escribir

# Etiqueta para mostrar errores
eti_errores = tk.Label(root, text="", fg="red")
eti_errores.pack()

# Etiqueta para mostrar el CAPTCHA
eti_captcha = tk.Label(root)
eti_captcha.pack()

# Campo para ingresar el texto del CAPTCHA
entrada_captcha = tk.Entry(root, width=30)

# Botón para iniciar sesión
btn_login = tk.Button(root, text="Iniciar Sesión", command=login, state="disabled")
btn_login.pack(pady=20)


# Función para abrir una nueva ventana después de un login exitoso
def abrir_nueva_ventana(nombre_usuario):
    logincorrecto = tk.Toplevel(root)
    logincorrecto.title("Datos correctos")
    
    # Establecer tamaño de la ventana
    logincorrecto.geometry("300x300")
    
    # Obtener las dimensiones de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Obtener las dimensiones de la ventana
    window_width = 300
    window_height = 300

    # Calcular la posición para centrar la ventana
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Establecer la geometría de la ventana con la posición calculada
    logincorrecto.geometry(f'{window_width}x{window_height}+{x}+{y}')
    
    # Agregar una etiqueta
    tk.Label(logincorrecto, text="Ha ingresado, bienvenido!!").pack(pady=20)

    # Crear el botón de "Usuarios" en esta ventana
    boton_usuarios = tk.Button(logincorrecto, text="Usuarios", command=abrir_ventana_de_usuarios)
    boton_usuarios.pack(pady=10)  # Añadir el botón a la nueva ventana
    
        # Crear el botón de "Productoss" en esta ventana
    boton_productos = tk.Button(logincorrecto, text="Productos", command=abrir_ventana_de_productos)
    boton_productos.pack(pady=10)  # Añadir el botón a la nueva ventana
        # Crear el botón de "Ventas" en esta ventana
  # Crear el botón de "Ventas" en esta ventana
    boton_ventas = tk.Button(logincorrecto, text="Ventas", command=abrir_ventana_de_ventas)
    boton_ventas.pack(pady=10)  # Añadir el botón a la nueva ventana
    
    # Crear el botón de "Reportes" en esta ventana
    boton_reportes = tk.Button(logincorrecto, text="Reportes", command=abrir_ventana_de_reportes)
    boton_reportes.pack(pady=10)  # Añadir el botón a la nueva ventana

# Función para abrir la ventana de usuarios
def abrir_ventana_de_usuarios():
    abrir_ventana_usuarios(root)  # Asegúrate de que esta función esté correctamente definida en usuarios.py

# Función para abrir la ventana de productos
def abrir_ventana_de_productos():
    abrir_ventana_productos(root)  # Asegúrate de que esta función esté correctamente definida en productos.py

# Función para abrir la ventana de ventas
def abrir_ventana_de_ventas():
    abrir_ventana_ventas(root, nombre_usuario)  # Asegúrate de que esta función esté correctamente definida en ventas.py

# Función para abrir la ventana de reportes
def abrir_ventana_de_reportes():
    abrir_ventana_reportes(root);

# Iniciar el loop principal de la aplicación
root.mainloop()