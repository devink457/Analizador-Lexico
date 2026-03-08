import tkinter as tk
from lexer import lexer
from parser import parser
from symbol_table import symbol_table, clear_table

COLOR_FONDO = "#4A9782"
COLOR_BOTON = "#004030"
COLOR_SEC = "#DCD0A8"
COLOR_TEXTO = "#EDEDCE"

def dibujar_arbol(arbol):
    ventana_arbol = tk.Toplevel()
    ventana_arbol.title("Árbol Sintáctico")

    canvas = tk.Canvas(ventana_arbol, width=1000, height=600, bg="white")
    canvas.pack(fill="both", expand=True)

    def dibujar_nodo(nodo, x, y, separacion):
        if nodo is None:
            return

        texto = str(nodo[0]) if isinstance(nodo, tuple) else str(nodo)

        canvas.create_oval(x-40, y-20, x+40, y+20, fill=COLOR_SEC)
        canvas.create_text(x, y, text=texto)

        if isinstance(nodo, tuple):
            hijos = nodo[1:]
            for i, hijo in enumerate(hijos):
                nuevo_x = x + (i - len(hijos)/2) * separacion
                nuevo_y = y + 80
                canvas.create_line(x, y+20, nuevo_x, nuevo_y-20)
                dibujar_nodo(hijo, nuevo_x, nuevo_y, separacion/2)

    dibujar_nodo(arbol, 500, 50, 300)

def analizar_lexico():
    salida.delete("1.0", tk.END)
    clear_table()

    codigo = editor.get("1.0", tk.END).strip()
    lexer.input(codigo)

    for token in lexer:
        salida.insert(tk.END, f"{token.type} -> {token.value}\n")

def analizar_sintactico():
    salida.delete("1.0", tk.END)
    codigo = editor.get("1.0", tk.END).strip()
    resultado = parser.parse(codigo)

    if resultado:
        salida.insert(tk.END, "Árbol generado correctamente\n")
        dibujar_arbol(resultado)

def mostrar_tabla():
    salida.delete("1.0", tk.END)
    for simbolo, info in symbol_table.items():
        salida.insert(tk.END, f"{simbolo} -> {info}\n")

def iniciar_gui():
    global editor, salida

    ventana = tk.Tk()
    ventana.title("Mini Compilador")
    ventana.configure(bg=COLOR_FONDO)

    tk.Label(ventana, text="Editor", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
    editor = tk.Text(ventana, height=10, width=80, bg=COLOR_SEC)
    editor.pack()

    frame = tk.Frame(ventana, bg=COLOR_FONDO)
    frame.pack()

    tk.Button(frame, text="Léxico", bg=COLOR_BOTON, fg=COLOR_TEXTO, command=analizar_lexico).grid(row=0, column=0)
    tk.Button(frame, text="Sintáctico", bg=COLOR_BOTON, fg=COLOR_TEXTO, command=analizar_sintactico).grid(row=0, column=1)
    tk.Button(frame, text="Tabla", bg=COLOR_BOTON, fg=COLOR_TEXTO, command=mostrar_tabla).grid(row=0, column=2)
    tk.Button(frame, text="Salir", bg="red", fg="white", command=ventana.quit).grid(row=0, column=3)

    salida = tk.Text(ventana, height=10, width=80, bg=COLOR_SEC)
    salida.pack()

    ventana.mainloop()