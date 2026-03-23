import tkinter as tk
from lexer import lexer
from parser import parser
from symbol_table import symbol_table, clear_table
from tkinter import messagebox

COLOR_FONDO = "#4A9782"
COLOR_BOTON = "#004030"
COLOR_SEC = "#DCD0A8"
COLOR_TEXTO = "#EDEDCE"

def dibujar_arbol(arbol):
    ventana_arbol = tk.Toplevel()
    ventana_arbol.title("Árbol Sintáctico")

    canvas = tk.Canvas(ventana_arbol, width=1200, height=700, bg="white")
    canvas.pack(fill="both", expand=True)

    # 🔹 calcular ancho del subárbol
    def ancho_subarbol(nodo):
        if not isinstance(nodo, tuple):
            return 1
        return sum(ancho_subarbol(h) for h in nodo[1:]) or 1

    def dibujar_nodo(nodo, x, y):
        if nodo is None:
            return

        texto = str(nodo[0]) if isinstance(nodo, tuple) else str(nodo)

        canvas.create_oval(x-40, y-20, x+40, y+20, fill=COLOR_SEC)
        canvas.create_text(x, y, text=texto)

        if isinstance(nodo, tuple):
            hijos = nodo[1:]
            total_ancho = sum(ancho_subarbol(h) for h in hijos)

            x_actual = x - total_ancho * 50  # separación base

            for hijo in hijos:
                ancho_hijo = ancho_subarbol(hijo)
                nuevo_x = x_actual + ancho_hijo * 50

                canvas.create_line(x, y+20, nuevo_x, y+80-20)
                dibujar_nodo(hijo, nuevo_x, y+80)

                x_actual += ancho_hijo * 100

    dibujar_nodo(arbol, 600, 50)

def analizar_lexico():
    salida.delete("1.0", tk.END)
    clear_table()

    from lexer import errores_lexicos
    errores_lexicos.clear()

    codigo = editor.get("1.0", tk.END).strip()
    lexer.input(codigo)

    for token in lexer:
        salida.insert(tk.END, f"{token.type} -> {token.value}\n")

    if errores_lexicos:
        salida.insert(tk.END, "\n")
        for e in errores_lexicos:
            salida.insert(tk.END, e + "\n")

def analizar_sintactico():
    salida.delete("1.0", tk.END)
    codigo = editor.get("1.0", tk.END).strip()

    from parser import errores
    errores.clear()

    resultado = parser.parse(codigo, lexer=lexer)

    if errores:
        mensaje = "\n".join(errores)
        messagebox.showerror("Errores Sintácticos", mensaje)
    else:
        salida.insert(tk.END, "Análisis correcto\n")
        dibujar_arbol(resultado)

def mostrar_tabla():
    salida.delete("1.0", tk.END)
    for simbolo, info in symbol_table.items():
        salida.insert(tk.END, f"{simbolo} -> {info}\n")

def iniciar_gui():
    global editor, salida

    ventana = tk.Tk()
    ventana.title("Mini Compilador")
    ventana.geometry("900x600")
    ventana.configure(bg="#1E1E1E")  # fondo oscuro

    # ======== EDITOR ========
    tk.Label(ventana, text="Editor de Código",
             bg="#1E1E1E", fg="#00FF9C", font=("Consolas", 12, "bold")).pack(pady=5)

    frame_editor = tk.Frame(ventana)
    frame_editor.pack(padx=10, pady=5)

    editor = tk.Text(
        frame_editor,
        height=12,
        width=100,
        bg="#252526",
        fg="white",
        insertbackground="white",
        font=("Consolas", 11),
        bd=0,
        relief="flat"
    )
    editor.pack(side=tk.LEFT)

    scroll_editor = tk.Scrollbar(frame_editor)
    scroll_editor.pack(side=tk.RIGHT, fill=tk.Y)

    editor.config(yscrollcommand=scroll_editor.set)
    scroll_editor.config(command=editor.yview)

    # ======== BOTONES ========
    frame_botones = tk.Frame(ventana, bg="#1E1E1E")
    frame_botones.pack(pady=10)

    def estilo_boton(btn):
        btn.configure(
            font=("Segoe UI", 10, "bold"),
            bg="#007ACC",
            fg="white",
            activebackground="#005F9E",
            activeforeground="white",
            bd=0,
            padx=10,
            pady=5
        )

    btn_lexico = tk.Button(frame_botones, text="Léxico", command=analizar_lexico)
    btn_sintactico = tk.Button(frame_botones, text="Sintáctico", command=analizar_sintactico)
    btn_tabla = tk.Button(frame_botones, text="Tabla", command=mostrar_tabla)
    btn_salir = tk.Button(frame_botones, text="Salir", command=ventana.quit, bg="#D32F2F")
    for btn in [btn_lexico, btn_sintactico, btn_tabla]:
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
    def on_enter_red(e):
        e.widget['bg'] = '#B71C1C'

    def on_leave_red(e):
        e.widget['bg'] = '#D32F2F'

    btn_salir.bind("<Enter>", on_enter_red)
    btn_salir.bind("<Leave>", on_leave_red)

    for i, btn in enumerate([btn_lexico, btn_sintactico, btn_tabla, btn_salir]):
        estilo_boton(btn)
        btn.grid(row=0, column=i, padx=10)

    # ======== SALIDA ========
    tk.Label(ventana, text="Salida",
             bg="#1E1E1E", fg="#00FF9C", font=("Consolas", 12, "bold")).pack()

    salida = tk.Text(
        ventana,
        height=10,
        width=100,
        bg="#111111",
        fg="#00FF9C",
        insertbackground="white",
        font=("Consolas", 10),
        bd=0
    )
    salida.pack(padx=10, pady=5)

    ventana.mainloop()
    
def on_enter(e):
    e.widget['bg'] = '#005F9E'

def on_leave(e):
    e.widget['bg'] = '#007ACC'
    


